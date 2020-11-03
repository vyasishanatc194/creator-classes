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

from customadmin.forms import MyCreatorClassChangeForm, MyCreatorClassCreationForm, ClassKeywordCreationForm, ClassKeywordChangeForm, ClassCoversCreationForm, ClassCoversChangeForm
from django.shortcuts import reverse

from creator.models import CreatorClass, ClassKeyword, ClassCovers

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

class CreatorClassListView(MyListView):
    """View for User listing"""

    # paginate_by = 25
    ordering = ["id"]
    model = CreatorClass
    queryset = model.objects.all()
    template_name = "customadmin/classes/creator_class_list.html"
    permission_required = ("customadmin.view_creator_class",)

    def get_queryset(self):
        return self.model.objects.all()

class ClassKeywordInline(InlineFormSetFactory):
    """Inline view to show Newsimage within the Parent View"""

    model = ClassKeyword
    form_class = ClassKeywordCreationForm
    factory_kwargs = {'extra': 4, 'max_num': None, 'can_order': False, 'can_delete': True}
class ClassCoversInline(InlineFormSetFactory):
    """Inline view to show Newsimage within the Parent View"""

    model = ClassCovers
    form_class = ClassCoversCreationForm
    factory_kwargs = {'extra': 2, 'max_num': None, 'can_order': False, 'can_delete': True}


class CreatorClassCreateView(MyNewFormsetCreateView):
    """View to create User"""

    model = CreatorClass

    inline_model = ClassKeyword, ClassCovers
    inlines = [ClassKeywordInline,ClassCoversInline ]

    form_class = MyCreatorClassCreationForm
    template_name = "customadmin/classes/creator_class_form.html"
    permission_required = ("customadmin.add_creator_class",)

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs["user"] = self.request.user 
    #     return kwargs

    def get_success_url(self):
        opts = self.model._meta
        return reverse("customadmin:creatorclass-list")

class ClassKeywordUpdateInline(InlineFormSetFactory):
    """View to update Newsimage which is a inline view"""

    model = ClassKeyword
    form_class = ClassKeywordChangeForm
    factory_kwargs = {'extra': 4, 'max_num': None, 'can_order': False, 'can_delete': True}

class ClassCoversUpdateInline(InlineFormSetFactory):
    """View to update Newsimage which is a inline view"""

    model = ClassCovers
    form_class = ClassCoversChangeForm
    factory_kwargs = {'extra': 2, 'max_num': None, 'can_order': False, 'can_delete': True}

class CreatorClassUpdateView(MyNewFormsetUpdateView):
    """View to update User"""

    model = CreatorClass

    inline_model = ClassKeyword, ClassCovers
    inlines = [ClassKeywordInline,ClassCoversInline ]


    form_class = MyCreatorClassChangeForm
    template_name = "customadmin/classes/creator_class_form_update.html"
    permission_required = ("customadmin.change_creator_class",)

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs["user"] = self.request.user
    #     return kwargs

    def get_success_url(self):
        opts = self.model._meta
        return reverse("customadmin:creatorclass-list")

class CreatorClassDeleteView(MyDeleteView):
    """View to delete User"""

    model = CreatorClass
    template_name = "customadmin/confirm_delete.html"
    permission_required = ("customadmin.delete_creator_class",)

    def get_success_url(self):
        opts = self.model._meta
        return reverse("customadmin:creatorclass-list")

class CreatorClassAjaxPagination(DataTableMixin, HasPermissionsMixin, MyLoginRequiredView):
    """Built this before realizing there is
    https://bitbucket.org/pigletto/django-datatables-view."""

    model = CreatorClass
    queryset = CreatorClass.objects.all().order_by("title")

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