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

from customadmin.forms import SessionBookingChangeForm, SessionBookingCreationForm, StreamBookingChangeForm, StreamBookingCreationForm
from django.shortcuts import reverse

from user.models import StreamBooking, SessionBooking, User, UserCard
from creator.models import TimeSlot, OneToOneSession, Creator
from django.http import JsonResponse

def GetSlots(request):
    creator_id = request.GET.get('creator_id')
    creator_obj = Creator.objects.filter(pk=creator_id).first()
    session_obj = OneToOneSession.objects.filter(creator=creator_obj).first()
    if session_obj:
        slots = TimeSlot.objects.filter(session=session_obj.pk).exclude(is_booked=True).values()
    else:
        slots =[]
    return JsonResponse(list(slots), content_type="application/json", safe=False)

def GetCards(request):
    user_id = request.GET.get('user_id')
    user_obj = User.objects.filter(pk=user_id).first()
    card_obj = UserCard.objects.filter(user=user_obj).values()
    return JsonResponse(list(card_obj), content_type="application/json", safe=False)

# -----------------------------------------------------------------------------
# Stream Booking
# -----------------------------------------------------------------------------

class StreamBookingListView(MyListView):
    """View for Stream Booking listing"""

    ordering = ["id"]
    model = StreamBooking
    queryset = model.objects.all()
    template_name = "customadmin/bookings/stream_booking_list.html"
    permission_required = ("customadmin.view_stream_booking",)

    def get_queryset(self):
        return self.model.objects.all().exclude(active=False)

class StreamBookingCreateView(MyCreateView):
    """View to create Stream booking"""

    model = StreamBooking
    context = {}

    form_class = StreamBookingCreationForm
    template_name = "customadmin/bookings/stream_booking_form.html"
    permission_required = ("customadmin.add_stream_booking",)

    def get_queryset(self):
        return self.model.objects.all().exclude(user.is_creator == true)

    def get_success_url(self):
        return reverse("customadmin:streambooking-list")

class StreamBookingUpdateView(MyUpdateView):
    """View to update Stream Booking"""

    model = StreamBooking
    form_class = StreamBookingChangeForm
    template_name = "customadmin/bookings/stream_booking_form.html"
    permission_required = ("customadmin.change_stream_booking",)

    def get_success_url(self):
        return reverse("customadmin:streambooking-list")

class StreamBookingDeleteView(MyDeleteView):
    """View to delete Stream Booking"""

    model = StreamBooking
    template_name = "customadmin/confirm_delete.html"
    permission_required = ("customadmin.delete_stream_booking",)

    def get_success_url(self):
        return reverse("customadmin:streambooking-list")

class StreamBookingAjaxPagination(DataTableMixin, HasPermissionsMixin, MyLoginRequiredView):
    """Built this before realizing there is
    https://bitbucket.org/pigletto/django-datatables-view."""

    model = StreamBooking
    queryset = StreamBooking.objects.all().order_by("created_at")

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
# Session Booking
# -----------------------------------------------------------------------------

class SessionBookingListView(MyListView):
    """View for Session Booking listing"""

    ordering = ["id"]
    model = SessionBooking
    queryset = model.objects.all()
    template_name = "customadmin/bookings/session_booking_list.html"
    permission_required = ("customadmin.view_session_booking",)

    def get_queryset(self):
        return self.model.objects.all().exclude(active=False)

class SessionBookingCreateView(MyCreateView):
    """View to create Session Booking"""

    model = SessionBooking
    context = {}

    form_class = SessionBookingCreationForm
    template_name = "customadmin/bookings/session_booking_form.html"
    permission_required = ("customadmin.add_session_booking",)

    def get_queryset(self):
        return self.model.objects.all().exclude(user.is_creator == true)

    def get_success_url(self):
        return reverse("customadmin:sessionbooking-list")

class SessionBookingUpdateView(MyUpdateView):
    """View to update Session Booking"""

    model = SessionBooking
    form_class = SessionBookingChangeForm
    template_name = "customadmin/bookings/session_booking_form.html"
    permission_required = ("customadmin.change_session_booking",)

    def get_success_url(self):
        return reverse("customadmin:sessionbooking-list")

class SessionBookingDeleteView(MyDeleteView):
    """View to delete Session Booking"""

    model = SessionBooking
    template_name = "customadmin/confirm_delete.html"
    permission_required = ("customadmin.delete_session_booking",)

    def get_success_url(self):
        return reverse("customadmin:sessionbooking-list")

class SessionBookingAjaxPagination(DataTableMixin, HasPermissionsMixin, MyLoginRequiredView):
    """Built this before realizing there is
    https://bitbucket.org/pigletto/django-datatables-view."""

    model = SessionBooking
    queryset = SessionBooking.objects.all().order_by("created_at")

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

