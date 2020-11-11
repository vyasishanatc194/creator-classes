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
from django.db.models import Q
from django.template.loader import get_template
from django_datatables_too.mixins import DataTableMixin

from customadmin.forms import AdminKeywordChangeForm, AdminKeywordCreationForm
from django.shortcuts import reverse

from ..models import AdminKeyword

# -----------------------------------------------------------------------------
# AdminKeywords
# -----------------------------------------------------------------------------

class AdminKeywordListView(MyListView):
    """View for AdminKeyword listing"""

    # paginate_by = 25
    ordering = ["id"]
    model = AdminKeyword
    queryset = model.objects.all()
    template_name = "customadmin/keywords/keyword_list.html"
    permission_required = ("customadmin.view_admin_keyword",)

    def get_queryset(self):
        return self.model.objects.all().exclude(active=False)

class AdminKeywordCreateView(MyCreateView):
    """View to create User"""

    model = AdminKeyword
    form_class = AdminKeywordCreationForm
    template_name = "customadmin/keywords/keyword_form.html"
    permission_required = ("customadmin.add_admin_keyword",)

    def get_success_url(self):
        opts = self.model._meta
        return reverse("customadmin:adminkeyword-list")

class AdminKeywordUpdateView(MyUpdateView):
    """View to update User"""

    model = AdminKeyword

    form_class = AdminKeywordChangeForm
    template_name = "customadmin/keywords/keyword_form.html"
    permission_required = ("customadmin.change_admin_keyword",)

    def get_success_url(self):
        opts = self.model._meta
        return reverse("customadmin:adminkeyword-list")

class AdminKeywordDeleteView(MyDeleteView):
    """View to delete User"""

    model = AdminKeyword
    template_name = "customadmin/confirm_delete.html"
    permission_required = ("customadmin.delete_admin_keyword",)

    def get_success_url(self):
        opts = self.model._meta
        return reverse("customadmin:adminkeyword-list")

class AdminKeywordAjaxPagination(DataTableMixin, HasPermissionsMixin, MyLoginRequiredView):
    """Built this before realizing there is
    https://bitbucket.org/pigletto/django-datatables-view."""

    model = AdminKeyword
    queryset = AdminKeyword.objects.all().order_by("created_at")

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