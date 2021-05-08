# -*- coding: utf-8 -*-
from customadmin.mixins import HasPermissionsMixin
from customadmin.views.generic import (
    MyCreateView,
    MyDeleteView,
    MyListView,
    MyDetailView,
    MyLoginRequiredView,
    MyUpdateView,
)
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Sum
from django.http import HttpResponse
from django.template.loader import get_template
from django.views.generic import TemplateView, DetailView
from django_datatables_too.mixins import DataTableMixin

from ..forms import MyUserChangeForm, MyUserCreationForm, UserCardChangeForm, UserCardCreationForm
from django.shortcuts import reverse, render

from creator.models import Stream, TimeSlot, CreatorTransferredMoney
from user.models import User, UserCard, SessionBooking, StreamBooking, UserPlanPurchaseHistory
from creator.models import Creator, CreatorAffiliation
from customadmin.models import CreatorClassCommission

import datetime

import csv

creator_class_commission = CreatorClassCommission.objects.all().first()
if not creator_class_commission:
    creator_class_commission = CreatorClassCommission()
    creator_class_commission.affiliation_deduction = 10
    creator_class_commission.creator_class_deduction = 10
    creator_class_commission.save()

# Export CSV FILE

def export_user_csv(request):

    output = []
    response = HttpResponse (content_type='text/csv')
    filename = u"User.csv"
    response['Content-Disposition'] = u'attachment; filename="{0}"'.format(filename)

    writer = csv.writer(response)
    query_set = User.objects.all()

    #Header
    writer.writerow(['Name', "Username",'Bio', 'Email', 'Status','Phone','User Type',"is_staff", "is_superuser","avatar","company"])
    for user in query_set:
        if user.groups.all():
            gp = user.groups.all()[0].name
        else:
            gp = None

        if not user.profile_image:
            avatar = None
        else:
            avatar = user.profile_image.url


        output.append([user.first_name, user.last_name, user.username, user.email, user.is_active,user.description,gp,user.is_staff, user.is_superuser, request.build_absolute_uri(avatar),])
    #CSV Data
    writer.writerows(output)
    return response

class UserDetailView(MyDetailView):
    template_name = "customadmin/adminuser/user_detail.html"
    context = {}

    def get(self, request, pk):
        self.context['user_detail'] = User.objects.filter(pk=pk).first()
        self.context['card_list'] = UserCard.objects.filter(user=pk)
        self.context['booked_session_list'] = SessionBooking.objects.filter(user=pk)
        self.context['booked_stream_list'] = StreamBooking.objects.filter(user=pk)
        return render(request, self.template_name, self.context)



class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "customadmin/index.html"
    context = {}

    def get(self, request):
        stream_bookings = StreamBooking.objects.all().aggregate(Sum("stream__stream_amount"))["stream__stream_amount__sum"]
        stream_earnings = (stream_bookings * creator_class_commission.creator_class_deduction / 100) if stream_bookings else 0

        session_bookings = SessionBooking.objects.all().aggregate(Sum("transaction_detail__amount"))["transaction_detail__amount__sum"]
        session_earnings = (session_bookings * creator_class_commission.creator_class_deduction / 100) if session_bookings else 0

        plan_purchase = UserPlanPurchaseHistory.objects.all().aggregate(Sum("plan_purchase_detail__amount"))["plan_purchase_detail__amount__sum"]
        commission_amount = CreatorAffiliation.objects.all().aggregate(Sum("commission_amount"))["commission_amount__sum"]
        plan_earnings = (plan_purchase if plan_purchase else 0) - (commission_amount if commission_amount else 0)

        creator_classes_earnings = stream_earnings + session_earnings + plan_earnings
        self.context['orders_count'] = []
        self.context['user_count']=User.objects.all().exclude(is_creator=True).exclude(username='admin').count()
        self.context['creator_count']=Creator.objects.all().filter(status='ACCEPT').count()
        self.context['creator_classes_earnings']=creator_classes_earnings
        self.context['pending_creator_count']=Creator.objects.filter(status='PENDING').count()
        self.context['live_stream'] = Stream.objects.filter(stream_datetime__gte=datetime.datetime.now()).count()
        self.context['transfer_money'] = CreatorTransferredMoney.objects.all().count()
        for i in range(1, 13):
            self.context['orders_count'].append(Stream.objects.filter(created_at__month=i).count())
        return render(request, self.template_name, self.context)

# -----------------------------------------------------------------------------
# Users
# -----------------------------------------------------------------------------


class UserListView(MyListView):
    """View for User listing"""

    model = User
    queryset = model.objects.exclude(username="admin").exclude(is_creator=True).order_by('-created_at')
    template_name = "customadmin/adminuser/user_list.html"
    permission_required = ("customadmin.view_user",)

    def get_queryset(self):
        return self.model.objects.exclude(username="admin").exclude(email=self.request.user).exclude(is_creator=True).order_by('-created_at')


class UserCreateView(MyCreateView):
    """View to create User"""

    model = User
    form_class = MyUserCreationForm
    template_name = "customadmin/adminuser/user_form.html"
    permission_required = ("customadmin.add_user",)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_success_url(self):
        # opts = self.model._meta
        return reverse("customadmin:user-list")

class UserUpdateView(MyUpdateView):
    """View to update User"""

    model = User
    form_class = MyUserChangeForm
    template_name = "customadmin/adminuser/user_form_update.html"
    permission_required = ("customadmin.change_user",)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_success_url(self):
        # opts = self.model._meta
        return reverse("customadmin:user-list")

class UserDeleteView(MyDeleteView):
    """View to delete User"""

    model = User
    template_name = "customadmin/confirm_delete.html"
    permission_required = ("customadmin.delete_user",)

    def get_success_url(self):
        # opts = self.model._meta
        return reverse("customadmin:user-list")

class UserPasswordView(MyUpdateView):
    """View to change User Password"""
    
    model = User
    form_class = AdminPasswordChangeForm
    template_name = "customadmin/adminuser/password_change_form.html"
    permission_required = ("customadmin.change_user",)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # kwargs['user'] = self.request.user
        kwargs["user"] = kwargs.pop("instance")
        return kwargs

    def get_success_url(self):
        opts = self.model._meta
        return reverse("customadmin:user-list")

class UserAjaxPagination(DataTableMixin, HasPermissionsMixin, MyLoginRequiredView):
    """Built this before realizing there is
    https://bitbucket.org/pigletto/django-datatables-view."""

    model = User
    queryset = User.objects.all().order_by("last_name")

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

# ------------------------------------------------------------------------------------
# User Card
# ------------------------------------------------------------------------------------

class UserCardListView(MyListView):
    """View for User Card listing"""

    ordering = ["id"]
    model = UserCard
    queryset = model.objects.all()
    template_name = "customadmin/adminuser/user_card_list.html"
    permission_required = ("customadmin.view_user",)

    def get_queryset(self):
        return self.model.objects.all()


class UserCardCreateView(MyCreateView):
    """View to create User Card"""

    model = UserCard
    form_class = UserCardCreationForm
    template_name = "customadmin/adminuser/user_card_form.html"
    permission_required = ("customadmin.add_user_card",)

    def get_success_url(self):
        # opts = self.model._meta
        return reverse("customadmin:usercard-list")

class UserCardUpdateView(MyUpdateView):
    """View to update User Card"""

    model = UserCard
    form_class = UserCardChangeForm
    template_name = "customadmin/adminuser/user_card_form.html"
    permission_required = ("customadmin.change_user_card",)

    def get_success_url(self):
        # opts = self.model._meta
        return reverse("customadmin:usercard-list")

class UserCardDeleteView(MyDeleteView):
    """View to delete User Card"""

    model = UserCard
    template_name = "customadmin/confirm_delete.html"
    permission_required = ("customadmin.delete_user_card",)

    def get_success_url(self):
        # opts = self.model._meta
        return reverse("customadmin:usercard-list")

class UserCardAjaxPagination(DataTableMixin, HasPermissionsMixin, MyLoginRequiredView):
    """Built this before realizing there is
    https://bitbucket.org/pigletto/django-datatables-view."""

    model = UserCard
    queryset = UserCard.objects.all()

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