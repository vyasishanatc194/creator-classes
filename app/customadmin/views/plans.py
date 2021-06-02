# -*- coding: utf-8 -*-
from customadmin.mixins import HasPermissionsMixin
from customadmin.views.generic import (
    MyDeleteView,
    MyListView,
    MyLoginRequiredView,
    MyDetailView,
    MyNewFormsetCreateView,
    MyNewFormsetUpdateView
)
from django.db.models import Q
from django.template.loader import get_template
from django_datatables_too.mixins import DataTableMixin

from customadmin.forms import PlanChangeForm, PlanCreationForm, PlanCoverCreationForm, PlanCoverChangeForm
from django.shortcuts import reverse, render

from ..models import Plan , PlanCover
from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSetFactory

from django.contrib import messages

MSG_CREATED = '"{}" created successfully.'
MSG_UPDATED = '"{}" updated successfully.'
MSG_DELETED = '"{}" deleted successfully.'
MSG_CANCELED = '"{}" canceled successfully.'

# -----------------------------------------------------------------------------
# Plan
# -----------------------------------------------------------------------------

class PlanDetailView(MyDetailView):
    model = Plan
    template_name = "customadmin/plans/plan_detail.html"
    permission_required = ("customadmin.view_plan_detail",)
    context = {}

    def get(self, request, pk):
        self.context['plan'] = pk
        self.context['plan_detail'] = Plan.objects.filter(pk=pk).first()
        self.context['plan_cover_list'] = PlanCover.objects.filter(plan=self.context['plan_detail'].pk)
        return render(request, self.template_name, self.context)

class PlanListView(MyListView):
    """View for Plan listing"""

    ordering = ["id"]
    model = Plan
    queryset = model.objects.all()
    template_name = "customadmin/plans/plan_list.html"
    permission_required = ("customadmin.view_plan",)

    def get_queryset(self):
        return self.model.objects.all().order_by('-created_at')

class PlanCoverInline(InlineFormSetFactory):
    """Inline view to show Cover within the Parent View"""

    model = PlanCover
    form_class = PlanCoverCreationForm
    factory_kwargs = {'extra': 6, 'max_num': None, 'can_order': False, 'can_delete': True}

class PlanCreateView(MyNewFormsetCreateView):
    """View to create Plan"""

    model = Plan
    inline_model = PlanCover
    inlines = [PlanCoverInline, ]
    form_class = PlanCreationForm
    template_name = "customadmin/plans/plan_form.html"
    permission_required = ("customadmin.add_plan",)

    def get_success_url(self):
        messages.success(self.request, MSG_UPDATED.format(self.object))
        return reverse("customadmin:plan-list")


class PlanCoverUpdateInline(InlineFormSetFactory):
    """View to update Cover which is a inline view"""

    model = PlanCover
    form_class = PlanCoverChangeForm
    factory_kwargs = {'extra': 6, 'max_num': None, 'can_order': False, 'can_delete': True}


class PlanDeleteView(MyDeleteView):
    """View to delete Plan"""

    model = Plan
    template_name = "customadmin/confirm_delete_plan.html"
    permission_required = ("customadmin.delete_plan",)

    def get_success_url(self):
        return reverse("customadmin:plan-list")

class PlanAjaxPagination(DataTableMixin, HasPermissionsMixin, MyLoginRequiredView):
    """Built this before realizing there is
    https://bitbucket.org/pigletto/django-datatables-view."""

    model = Plan
    queryset = Plan.objects.all().order_by("created_at")

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