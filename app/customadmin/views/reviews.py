# -*- coding: utf-8 -*-
from customadmin.mixins import HasPermissionsMixin
from customadmin.views.generic import (
    MyCreateView,
    MyDeleteView,
    MyListView,
    MyLoginRequiredView,
    MyUpdateView,
)
from django.db.models import Q
from django.template.loader import get_template
from django_datatables_too.mixins import DataTableMixin

from customadmin.forms import MyCreatorReviewChangeForm, MyCreatorReviewCreationForm, MyClassReviewChangeForm, MyClassReviewCreationForm
from django.shortcuts import reverse

from user.models import CreatorReview, ClassReview
# -----------------------------------------------------------------------------
# CreatorReviews
# -----------------------------------------------------------------------------

class CreatorReviewListView(MyListView):
    """View for CreatorReviews listing"""

    ordering = ["id"]
    model = CreatorReview
    queryset = model.objects.all()
    template_name = "customadmin/reviews/creator_review_list.html"
    permission_required = ("customadmin.view_creator_review",)

    def get_queryset(self):
        return self.model.objects.all().exclude(active=False).order_by('-created_at')

class CreatorReviewCreateView(MyCreateView):
    """View to create CreatorReviews"""

    model = CreatorReview
    context = {}
    form_class = MyCreatorReviewCreationForm
    template_name = "customadmin/reviews/creator_review_form.html"
    permission_required = ("customadmin.add_creator_review",)

    def get_queryset(self):
        return self.model.objects.all().exclude(user.is_creator == true)

    def get_success_url(self):
        return reverse("customadmin:creatorreview-list")

class CreatorReviewUpdateView(MyUpdateView):
    """View to update CreatorReviews"""

    model = CreatorReview
    form_class = MyCreatorReviewChangeForm
    template_name = "customadmin/reviews/creator_review_form.html"
    permission_required = ("customadmin.change_creator_review",)

    def get_success_url(self):
        return reverse("customadmin:creatorreview-list")

class CreatorReviewDeleteView(MyDeleteView):
    """View to delete CreatorReviews"""

    model = CreatorReview
    template_name = "customadmin/confirm_delete.html"
    permission_required = ("customadmin.delete_creator_review",)

    def get_success_url(self):
        return reverse("customadmin:creatorreview-list")

class CreatorReviewAjaxPagination(DataTableMixin, HasPermissionsMixin, MyLoginRequiredView):
    """Built this before realizing there is
    https://bitbucket.org/pigletto/django-datatables-view."""

    model = CreatorReview
    queryset = CreatorReview.objects.all().order_by("created_at")

    def _get_is_superuser(self, obj):
        """Get boolean column markup."""
        t = get_template("customadmin/partials/list_boolean.html")
        return t.render({"bool_val": obj.is_superuser})

    def _get_actions(self, obj, **kwargs):
        """Get actions column markup."""
        # ctx = super().get_context_data(**kwargs)
        t = get_template("customadmin/partials/list_basic_actions.html")
        # ctx.update({"obj": obj})
        # print(ctx)
        return t.render({"o": obj})

    def filter_queryset(self, qs):
        """Return the list of items for this view."""
        # If a search term, filter the query
        if self.search:
            return qs.filter(
                Q(username__icontains=self.search)
                | Q(first_name__icontains=self.search)
                | Q(last_name__icontains=self.search)
                # | Q(state__icontains=self.search)
                # | Q(year__icontains=self.search)
            )
        return qs

    def prepare_results(self, qs):
        # Create row data for datatables
        data = []
        for o in qs:
            data.append(
                {
                    "username": o.username,
                    "first_name": o.first_name,
                    "last_name": o.last_name,
                    "is_superuser": self._get_is_superuser(o),
                    # "modified": o.modified.strftime("%b. %d, %Y, %I:%M %p"),
                    "actions": self._get_actions(o),
                }
            )
        return data


# -----------------------------------------------------------------------------
# ClassReviews
# -----------------------------------------------------------------------------

class ClassReviewListView(MyListView):
    """View for ClassReviews listing"""

    ordering = ["id"]
    model = ClassReview
    queryset = model.objects.all()
    template_name = "customadmin/reviews/class_review_list.html"
    permission_required = ("customadmin.view_class_review",)

    def get_queryset(self):
        return self.model.objects.all().exclude(active=False).order_by('-created_at')

class ClassReviewCreateView(MyCreateView):
    """View to create ClassReviews"""

    model = ClassReview
    context = {}
    form_class = MyClassReviewCreationForm
    template_name = "customadmin/reviews/class_review_form.html"
    permission_required = ("customadmin.add_class_review",)

    def get_queryset(self):
        return self.model.objects.all().exclude(user.is_creator == true)

    def get_success_url(self):
        return reverse("customadmin:classreview-list")

class ClassReviewUpdateView(MyUpdateView):
    """View to update ClassReviews"""

    model = ClassReview
    form_class = MyClassReviewChangeForm
    template_name = "customadmin/reviews/class_review_form.html"
    permission_required = ("customadmin.change_class_review",)

    def get_success_url(self):
        return reverse("customadmin:classreview-list")

class ClassReviewDeleteView(MyDeleteView):
    """View to delete ClassReviews"""

    model = ClassReview
    template_name = "customadmin/confirm_delete.html"
    permission_required = ("customadmin.delete_class_review",)

    def get_success_url(self):
        return reverse("customadmin:classreview-list")

class ClassReviewAjaxPagination(DataTableMixin, HasPermissionsMixin, MyLoginRequiredView):
    """Built this before realizing there is
    https://bitbucket.org/pigletto/django-datatables-view."""

    model = ClassReview
    queryset = ClassReview.objects.all().order_by("created_at")

    def _get_is_superuser(self, obj):
        """Get boolean column markup."""
        t = get_template("customadmin/partials/list_boolean.html")
        return t.render({"bool_val": obj.is_superuser})

    def _get_actions(self, obj, **kwargs):
        """Get actions column markup."""
        # ctx = super().get_context_data(**kwargs)
        t = get_template("customadmin/partials/list_basic_actions.html")
        # ctx.update({"obj": obj})
        # print(ctx)
        return t.render({"o": obj})

    def filter_queryset(self, qs):
        """Return the list of items for this view."""
        # If a search term, filter the query
        if self.search:
            return qs.filter(
                Q(username__icontains=self.search)
                | Q(first_name__icontains=self.search)
                | Q(last_name__icontains=self.search)
                # | Q(state__icontains=self.search)
                # | Q(year__icontains=self.search)
            )
        return qs

    def prepare_results(self, qs):
        # Create row data for datatables
        data = []
        for o in qs:
            data.append(
                {
                    "username": o.username,
                    "first_name": o.first_name,
                    "last_name": o.last_name,
                    "is_superuser": self._get_is_superuser(o),
                    # "modified": o.modified.strftime("%b. %d, %Y, %I:%M %p"),
                    "actions": self._get_actions(o),
                }
            )
        return data
