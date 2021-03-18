# -*- coding: utf-8 -*-
from customadmin.mixins import HasPermissionsMixin
from customadmin.views.generic import (
    MyDeleteView,
    MyListView,
    MyLoginRequiredView,
    MyUpdateView,
    MyDetailView,
    MyNewFormsetCreateView,
    MyNewFormsetUpdateView
)
from django.db.models import Q
from django.template.loader import get_template
from django_datatables_too.mixins import DataTableMixin

from customadmin.forms import OneToOneSessionChangeForm, OneToOneSessionCreationForm, TimeSlotCreationForm, TimeSlotChangeForm
from django.shortcuts import reverse, render

from creator.models import OneToOneSession , TimeSlot
from user.models import SessionBooking

from extra_views import InlineFormSetFactory
from django.contrib import messages

MSG_CREATED = '"{}" created successfully.'
MSG_UPDATED = '"{}" updated successfully.'
MSG_DELETED = '"{}" deleted successfully.'
MSG_CANCELED = '"{}" canceled successfully.'

# -----------------------------------------------------------------------------
# OneToOneSessions
# -----------------------------------------------------------------------------

class OneToOneSessionDetailView(MyDetailView):
    model = OneToOneSession
    template_name = "customadmin/sessions/session_detail.html"
    permission_required = ("customadmin.view_session_detail",)
    context = {}

    def get(self, request, pk):
        self.context['session_detail'] = OneToOneSession.objects.filter(pk=pk).first()
        self.context['slot_detail'] = TimeSlot.objects.filter(session=pk)
        self.context['session_booking_detail'] = SessionBooking.objects.all()
        return render(request, self.template_name, self.context)

class OneToOneSessionListView(MyListView):
    """View for OneToOneSession listing"""

    ordering = ["id"]
    model = OneToOneSession
    queryset = model.objects.all()
    template_name = "customadmin/sessions/session_list.html"
    permission_required = ("customadmin.view_session",)

    def get_queryset(self):
        return self.model.objects.all().order_by('-created_at')

class TimeSlotInline(InlineFormSetFactory):
    """Inline view to show TimeSlot within the Parent View"""

    model = TimeSlot
    form_class = TimeSlotCreationForm
    factory_kwargs = {'extra': 4, 'max_num': 4, 'can_order': False, 'can_delete': True}

class OneToOneSessionCreateView(MyNewFormsetCreateView):
    """View to create OneToOneSessions"""

    model = OneToOneSession
    inline_model = TimeSlot
    inlines = [TimeSlotInline, ]
    form_class = OneToOneSessionCreationForm
    template_name = "customadmin/sessions/session_form.html"
    permission_required = ("customadmin.add_session",)

    def get_success_url(self):
        messages.success(self.request, MSG_CREATED.format(self.object))
        return reverse("customadmin:onetoonesession-list")

class TimeSlotUpdateInline(InlineFormSetFactory):
    """View to update TimeSlot which is a inline view"""

    model = TimeSlot
    form_class = TimeSlotChangeForm
    factory_kwargs = {'extra': 4, 'max_num': 4, 'can_order': False, 'can_delete': True}

class OneToOneSessionUpdateView(MyNewFormsetUpdateView):
    """View to update OneToOneSessions"""

    model = OneToOneSession
    inline_model = TimeSlot
    inlines = [TimeSlotInline, ]
    form_class = OneToOneSessionChangeForm
    template_name = "customadmin/sessions/session_form.html"
    permission_required = ("customadmin.change_session",)

    def get_success_url(self):
        messages.success(self.request, MSG_UPDATED.format(self.object))
        return reverse("customadmin:onetoonesession-list")

class OneToOneSessionDeleteView(MyDeleteView):
    """View to delete OneToOneSessions"""

    model = OneToOneSession
    template_name = "customadmin/confirm_delete.html"
    permission_required = ("customadmin.delete_sessions",)

    def get_success_url(self):
        return reverse("customadmin:onetoonesession-list")

class OneToOneSessionAjaxPagination(DataTableMixin, HasPermissionsMixin, MyLoginRequiredView):
    """Built this before realizing there is
    https://bitbucket.org/pigletto/django-datatables-view."""

    model = OneToOneSession
    queryset = OneToOneSession.objects.all().order_by("created_at")

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