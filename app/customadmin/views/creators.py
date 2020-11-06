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

from customadmin.forms import MyCreatorChangeForm, MyCreatorCreationForm, CreatorSkillCreationForm, CreatorSkillChangeForm
from django.shortcuts import reverse

from creator.models import Creator , CreatorSkill

from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSetFactory


import csv


# User = get_user_model()


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
        if creator.groups.all():
            gp = creator.groups.all()[0].name
        else:
            gp = None 

        if not creator.profile_image:
            avatar = None
        else:
            avatar = creator.profile_image.url


        output.append([creator.email, creator.username, creator.first_name, creator.last_name,request.build_absolute_uri(avatar), creator.description, creator.is_active, creator.is_staff, creator.is_superuser, creator.key_skill, creator.instagram_url, creator.linkedin_url, creator.twitter_url, creator.google_url, creator.facebook_url ,])
    #CSV Data
    writer.writerows(output)
    return response




# -----------------------------------------------------------------------------
# Users
# -----------------------------------------------------------------------------

class CreatorListView(MyListView):
    """View for Creator listing"""

    # paginate_by = 25
    ordering = ["id"]
    model = Creator
    queryset = model.objects.all()
    template_name = "customadmin/creator/creator_list.html"
    permission_required = ("customadmin.view_creator",)

    def get_queryset(self):
        return self.model.objects.all()

class CreatorSkillInline(InlineFormSetFactory):
    """Inline view to show Newsimage within the Parent View"""

    model = CreatorSkill
    form_class = CreatorSkillCreationForm
    factory_kwargs = {'extra': 1, 'max_num': None, 'can_order': False, 'can_delete': True}


class CreatorCreateView(MyNewFormsetCreateView):
    """View to create User"""

    model = Creator

    inline_model = CreatorSkill
    inlines = [CreatorSkillInline, ]

    form_class = MyCreatorCreationForm
    template_name = "customadmin/creator/creator_form.html"
    permission_required = ("customadmin.add_creator",)

    def get_success_url(self):
        opts = self.model._meta
        return reverse("customadmin:creator-list")

class CreatorSkillUpdateInline(InlineFormSetFactory):
    """View to update Newsimage which is a inline view"""

    model = CreatorSkill
    form_class = CreatorSkillChangeForm
    factory_kwargs = {'extra': 1, 'max_num': None, 'can_order': False, 'can_delete': True}

class CreatorUpdateView(MyNewFormsetUpdateView):
    """View to update User"""

    model = Creator

    inline_model = CreatorSkill
    inlines = [CreatorSkillInline, ]


    form_class = MyCreatorChangeForm
    template_name = "customadmin/creator/creator_form_update.html"
    permission_required = ("customadmin.change_creator",)

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs["user"] = self.request.user
    #     return kwargs

    def get_success_url(self):
        opts = self.model._meta
        return reverse("customadmin:creator-list")

class CreatorDeleteView(MyDeleteView):
    """View to delete User"""

    model = Creator
    template_name = "customadmin/confirm_delete.html"
    permission_required = ("customadmin.delete_creator",)

    def get_success_url(self):
        opts = self.model._meta
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