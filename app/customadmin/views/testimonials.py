# -*- coding: utf-8 -*-
from customadmin.mixins import HasPermissionsMixin
from customadmin.views.generic import (
    MyCreateView,
    MyDeleteView,
    MyListView,
    MyLoginRequiredView,
    MyUpdateView,
    MyView,
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

from customadmin.forms import TestimonialChangeForm, TestimonialCreationForm
from django.shortcuts import reverse

from ..models import Testimonial

# -----------------------------------------------------------------------------
# Testimonials
# -----------------------------------------------------------------------------

class TestimonialListView(MyListView):
    """View for User listing"""

    # paginate_by = 25
    ordering = ["id"]
    model = Testimonial
    queryset = model.objects.all()
    template_name = "customadmin/testimonials/testimonial_list.html"
    permission_required = ("customadmin.view_testimonial",)

    def get_queryset(self):
        return self.model.objects.all().exclude(active=False)

class TestimonialCreateView(MyCreateView):
    """View to create User"""

    model = Testimonial
    form_class = TestimonialCreationForm
    template_name = "customadmin/testimonials/testimonial_form.html"
    permission_required = ("customadmin.add_testimonial",)

    def get_success_url(self):
        opts = self.model._meta
        return reverse("customadmin:testimonial-list")

class TestimonialUpdateView(MyUpdateView):
    """View to update User"""

    model = Testimonial

    form_class = TestimonialChangeForm
    template_name = "customadmin/testimonials/testimonial_form.html"
    permission_required = ("customadmin.change_testimonial",)

    def get_success_url(self):
        opts = self.model._meta
        return reverse("customadmin:testimonial-list")

class TestimonialDeleteView(MyDeleteView):
    """View to delete User"""

    model = Testimonial
    template_name = "customadmin/confirm_delete.html"
    permission_required = ("customadmin.delete_testimonial",)

    def get_success_url(self):
        opts = self.model._meta
        return reverse("customadmin:testimonial-list")

class TestimonialAjaxPagination(DataTableMixin, HasPermissionsMixin, MyLoginRequiredView):
    """Built this before realizing there is
    https://bitbucket.org/pigletto/django-datatables-view."""

    model = Testimonial
    queryset = Testimonial.objects.all().order_by("created_at")

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