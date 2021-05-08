from customadmin.mixins import HasPermissionsMixin
from customadmin.views.generic import (
    MyCreateView,
    MyDeleteView,
    MyListView,
    MyDetailView,
    MyLoginRequiredView,
    MyUpdateView,
)
from ..models import AvailableTimezone
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Sum
from django.http import HttpResponse
from django.template.loader import get_template
from django.views.generic import TemplateView, DetailView
from django_datatables_too.mixins import DataTableMixin

from ..forms import TimezoneCreateForm
from django.shortcuts import reverse, render

import datetime

class TimezoneListView(MyListView):
    """View for User listing"""

    model = AvailableTimezone
    queryset = model.objects.all().order_by('-created_at')
    template_name = "customadmin/timezone/timezone_list.html"

    def get_queryset(self):
        return self.model.objects.order_by('-created_at')


class TimezoneCreateView(MyCreateView):
    """View to create User"""

    model = AvailableTimezone
    form_class = TimezoneCreateForm
    template_name = "customadmin/timezone/timezone_form.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        return kwargs

    def get_success_url(self):
        # opts = self.model._meta
        return reverse("customadmin:availabletimezone-list")


class TimezoneUpdateView(MyUpdateView):
    """View to update User"""

    model = AvailableTimezone
    form_class = TimezoneCreateForm
    template_name = "customadmin/timezone/timezone_form.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        return kwargs

    def get_success_url(self):
        # opts = self.model._meta
        return reverse("customadmin:availabletimezone-list")


class TimezoneDeleteView(MyDeleteView):
    """View to delete User"""

    model = AvailableTimezone
    template_name = "customadmin/confirm_delete.html"

    def get_success_url(self):
        # opts = self.model._meta
        return reverse("customadmin:availabletimezone-list")