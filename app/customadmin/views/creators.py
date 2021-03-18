# -*- coding: utf-8 -*-
from customadmin.mixins import HasPermissionsMixin
from customadmin.views.generic import (
    MyDeleteView,
    MyListView,
    MyDetailView,
    MyLoginRequiredView,
    MyNewFormsetCreateView,
    MyNewFormsetUpdateView
)
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from django_datatables_too.mixins import DataTableMixin

from customadmin.forms import MyCreatorChangeForm, MyCreatorCreationForm, CreatorSkillCreationForm, CreatorSkillChangeForm
from django.shortcuts import reverse, render

from creator.models import Creator , CreatorSkill, Material, CreatorClass, OneToOneSession, TimeSlot, Stream
from user.models import CreatorReview
from extra_views import InlineFormSetFactory
from django.views.generic import DetailView

import csv
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings 

MSG_CREATED = '"{}" created successfully.'
MSG_UPDATED = '"{}" updated successfully.'
MSG_DELETED = '"{}" deleted successfully.'
MSG_CANCELED = '"{}" canceled successfully.'

# Export CSV FILE

def creator_export_product_csv(request):

    output = []
    response = HttpResponse (content_type='text/csv')
    filename = u"Creator.csv"
    response['Content-Disposition'] = u'attachment; filename="{0}"'.format(filename)
    writer = csv.writer(response)
    query_set = Creator.objects.all()

    #Header
    writer.writerow(['Email', "Username",'Firstname', 'Lastname', 'Profile Image','Description','is_active',"is_staff", "is_superuser","Key Skill","Instagram", "LinkedIn", "Twitter", "Google", "Facebook"])
    for creator in query_set:
        if not creator.profile_image:
            avatar = None
        else:
            avatar = creator.profile_image.url


        output.append([creator.email, creator.username, creator.first_name, creator.last_name,request.build_absolute_uri(avatar), creator.description, creator.is_active, creator.is_staff, creator.is_superuser, creator.key_skill, creator.instagram_url, creator.linkedin_url, creator.twitter_url, creator.google_url, creator.facebook_url ,])
    #CSV Data
    writer.writerows(output)
    return response

# -----------------------------------------------------------------------------
# Creators
# -----------------------------------------------------------------------------

def CreatorRejectRequestAjax(request):
    pk = request.GET.get('creator_id',False)
    creator_obj = Creator.objects.get(pk=pk)
    if creator_obj:
        creator_obj.status = 'REJECT'
        if creator_obj.is_active:
            creator_obj.is_active = False
        creator_obj.save()
        subject = 'Request rejected !!!'
        message = f'Hi {creator_obj.username}, your request is rejected by creatorclass admin.'
        email_from = settings.EMAIL_HOST_USER 
        recipient_list = [creator_obj.email, ] 
        send_mail( subject, message, email_from, recipient_list )
        messages.success(request, "'Request rejected successfully'")
    return JsonResponse({"success": True})

def CreatorAcceptRequestAjax(request):
    pk = request.GET.get('creator_id',False)
    creator_obj = Creator.objects.get(pk=pk)
    if creator_obj:
        creator_obj.status = 'ACCEPT'
        if not creator_obj.is_active:
            creator_obj.is_active = True
        creator_obj.save()
        subject = 'Request Accepted !!!'
        message = f'Hi {creator_obj.username}, your request is accepted by creatorclass admin.'
        email_from = settings.EMAIL_HOST_USER 
        recipient_list = [creator_obj.email, ] 
        send_mail( subject, message, email_from, recipient_list ) 
        messages.success(request, "'Request accept successfully'")
    return JsonResponse({"success": True})

class CreatorDetailView(MyDetailView):
    model = Creator
    template_name = "customadmin/creator/creator_detail.html"
    permission_required = ("customadmin.view_creator_detail",)
    context = {}

    def get(self, request, pk):
        avg_class_review = 0
        self.context['creator'] = Creator.objects.filter(pk=pk).first()
        self.context['class_list'] = CreatorClass.objects.filter(creator=pk)
        self.context['session_list'] = OneToOneSession.objects.filter(creator=pk)
        self.context['material_list'] = Material.objects.filter(creator=pk)
        self.context['creator_review_list'] = CreatorReview.objects.filter(creator=pk)
        self.context['session_slot_list'] = TimeSlot.objects.all()
        self.context['stream_list'] = Stream.objects.filter(creator=pk)
        self.context['other_skill'] = CreatorSkill.objects.filter(creator=pk)
        if self.context['creator_review_list']:
            for review in self.context['creator_review_list']:
                avg_class_review += review.rating
            self.context['avg_class_review']= avg_class_review/len(self.context['creator_review_list'])
        else:
            self.context['avg_class_review']= 0
        return render(request, self.template_name, self.context)


class CreatorListView(MyListView):
    """View for Creator listing"""

    model = Creator
    queryset = model.objects.all().order_by('-created_at')
    template_name = "customadmin/creator/creator_list.html"
    permission_required = ("customadmin.view_creator",)

    def get_queryset(self):
        return self.model.objects.all().order_by('-created_at')

class CreatorSkillInline(InlineFormSetFactory):
    """Inline view to show Skill within the Parent View"""

    model = CreatorSkill
    form_class = CreatorSkillCreationForm
    factory_kwargs = {'extra': 1, 'max_num': None, 'can_order': False, 'can_delete': True}

class CreatorCreateView(MyNewFormsetCreateView):
    """View to create Creator"""

    model = Creator
    inline_model = CreatorSkill
    inlines = [CreatorSkillInline, ]
    form_class = MyCreatorCreationForm
    template_name = "customadmin/creator/creator_form.html"
    permission_required = ("customadmin.add_creator",)

    def get_success_url(self):
        messages.success(self.request, MSG_CREATED.format(self.object))
        return reverse("customadmin:creator-list")

class CreatorSkillUpdateInline(InlineFormSetFactory):
    """View to update Skill which is a inline view"""

    model = CreatorSkill
    form_class = CreatorSkillChangeForm
    factory_kwargs = {'extra': 1, 'max_num': None, 'can_order': False, 'can_delete': True}

class CreatorUpdateView(MyNewFormsetUpdateView):
    """View to update Creator"""

    model = Creator
    inline_model = CreatorSkill
    inlines = [CreatorSkillInline, ]
    form_class = MyCreatorChangeForm
    template_name = "customadmin/creator/creator_form_update.html"
    permission_required = ("customadmin.change_creator",)

    def get_success_url(self):
        messages.success(self.request, MSG_UPDATED.format(self.object))
        return reverse("customadmin:creator-list")

class CreatorDeleteView(MyDeleteView):
    """View to delete Creator"""

    model = Creator
    template_name = "customadmin/confirm_delete.html"
    permission_required = ("customadmin.delete_creator",)

    def get_success_url(self):
        return reverse("customadmin:creator-list")

class CreatorAjaxPagination(DataTableMixin, HasPermissionsMixin, MyLoginRequiredView):
    """Built this before realizing there is
    https://bitbucket.org/pigletto/django-datatables-view."""

    model = Creator
    queryset = Creator.objects.all().order_by("key_skill")

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