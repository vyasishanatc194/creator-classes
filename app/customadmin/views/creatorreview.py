# -*- coding: utf-8 -*-
from customadmin.mixins import HasPermissionsMixin
from customadmin.views.generic import (
    MyCreateView,
    MyDeleteView,
    MyListView,
    MyLoginRequiredView,
    MyUpdateView,
    MyView,
    MyNewFormsetCreateView,
    MyNewFormsetUpdateView
)
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.template.loader import get_template
from django.utils.text import Truncator
from django.views.generic import TemplateView
from django_datatables_too.mixins import DataTableMixin

from customadmin.forms import MyCreatorReviewChangeForm, MyCreatorReviewCreationForm
from django.shortcuts import reverse

from user.models import CreatorReview




# -----------------------------------------------------------------------------
# CreatorReviews
# -----------------------------------------------------------------------------

class CreatorReviewListView(MyListView):
    """View for User listing"""

    # paginate_by = 25
    ordering = ["id"]
    model = CreatorReview
    queryset = model.objects.all()
    template_name = "customadmin/reviews/creator_review_list.html"
    permission_required = ("customadmin.view_creator_review",)

    def get_queryset(self):
        return self.model.objects.all()


class CreatorReviewCreateView(MyNewFormsetCreateView):
    """View to create User"""

    model = CreatorReview

    form_class = MyCreatorReviewCreationForm
    template_name = "customadmin/reviews/creator_review_form.html"
    permission_required = ("customadmin.add_creator_review",)

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs["user"] = self.request.user 
    #     return kwargs

    def get_success_url(self):
        opts = self.model._meta
        return reverse("customadmin:creatorreview-list")


class CreatorReviewUpdateView(MyNewFormsetUpdateView):
    """View to update User"""

    model = CreatorReview

    form_class = MyCreatorReviewChangeForm
    template_name = "customadmin/reviews/creator_review_form_update.html"
    permission_required = ("customadmin.change_creator_review",)

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs["user"] = self.request.user
    #     return kwargs

    def get_success_url(self):
        opts = self.model._meta
        return reverse("customadmin:creatorreview-list")

class CreatorReviewDeleteView(MyDeleteView):
    """View to delete User"""

    model = CreatorReview
    template_name = "customadmin/confirm_delete.html"
    permission_required = ("customadmin.delete_creator_review",)

    def get_success_url(self):
        opts = self.model._meta
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