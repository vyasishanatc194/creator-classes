# -*- coding: utf-8 -*-
from customadmin.mixins import HasPermissionsMixin
from customadmin.views.generic import (
    MyDeleteView,
    MyListView,
    MyLoginRequiredView,
    MyView,
    MyNewFormsetCreateView,
    MyNewFormsetUpdateView
)
from django.db.models import Q
from django.http import JsonResponse
from django.template.loader import get_template
from django_datatables_too.mixins import DataTableMixin
from django.views.generic import DetailView

from customadmin.forms import MyCreatorClassChangeForm, MyCreatorClassCreationForm, ClassKeywordCreationForm, ClassKeywordChangeForm, ClassCoversCreationForm, ClassCoversChangeForm, ClassMaterialCreationForm, ClassMaterialChangeForm
from django.shortcuts import reverse, render

from creator.models import CreatorClass, ClassKeyword, ClassCovers, ClassMaterial
from user.models import ClassReview
from extra_views import InlineFormSetFactory

from django.contrib import messages

MSG_CREATED = '"{}" created successfully.'
MSG_UPDATED = '"{}" updated successfully.'
MSG_DELETED = '"{}" deleted successfully.'
MSG_CANCELED = '"{}" canceled successfully.'

from creator.models import Material
def GetMaterials(request):
    creator_id = request.GET.get('creator_id')
    materials = Material.objects.filter(creator=creator_id).values()
    return JsonResponse(list(materials), content_type="application/json", safe=False)

# -----------------------------------------------------------------------------
# Creator Classes
# -----------------------------------------------------------------------------

class ClassDetailView(DetailView):
    model = CreatorClass
    template_name = "customadmin/classes/class_detail.html"
    permission_required = ("customadmin.view_class_detail",)
    context = {}

    def get(self, request, pk):
        self.context['class_detail'] = CreatorClass.objects.filter(pk=pk).first()
        self.context['class_file_url'] = request.build_absolute_uri(self.context['class_detail'].class_file) 
        self.context['class_file_url'] = self.context['class_file_url'][:22] + 'media' + self.context['class_file_url'][50:]
        self.context['class_keyword_list'] = ClassKeyword.objects.filter(creator_class=pk)
        self.context['class_cover_list'] = ClassCovers.objects.filter(creator_class=pk)
        self.context['class_material_list'] = ClassMaterial.objects.filter(creator_class=pk)
        self.context['class_review_list'] = ClassReview.objects.filter(creator_class=pk)
        return render(request, self.template_name, self.context)

class CreatorClassListView(MyListView):
    """View for Creator Class listing"""

    # paginate_by = 25
    ordering = ["id"]
    model = CreatorClass
    queryset = model.objects.all()
    template_name = "customadmin/classes/creator_class_list.html"
    permission_required = ("customadmin.view_creator_class",)

    def get_queryset(self):
        return self.model.objects.all().exclude(active=False)


class ClassMaterialInline(InlineFormSetFactory):
    """Inline view to show Newsimage within the Parent View"""

    model = ClassMaterial
    form_class = ClassMaterialCreationForm
    factory_kwargs = {'extra': 4, 'max_num': 4, 'can_order': False, 'can_delete': True}

class ClassKeywordInline(InlineFormSetFactory):
    """Inline view to show Newsimage within the Parent View"""

    model = ClassKeyword
    form_class = ClassKeywordCreationForm
    factory_kwargs = {'extra': 4, 'max_num': 4, 'can_order': False, 'can_delete': True}

class ClassCoversInline(InlineFormSetFactory):
    """Inline view to show Newsimage within the Parent View"""

    model = ClassCovers
    form_class = ClassCoversCreationForm
    factory_kwargs = {'extra': 4, 'max_num': 4, 'can_order': False, 'can_delete': True}

class CreatorClassCreateView(MyNewFormsetCreateView):
    """View to create User"""

    model = CreatorClass

    inlines = [ClassKeywordInline,ClassCoversInline, ClassMaterialInline,]

    form_class = MyCreatorClassCreationForm
    template_name = "customadmin/classes/creator_class_form.html"
    permission_required = ("customadmin.add_creator_class",)

    def get_success_url(self):
        messages.success(self.request, MSG_CREATED.format(self.object))
        # opts = self.model._meta
        return reverse("customadmin:creatorclass-list") 

class ClassKeywordUpdateInline(InlineFormSetFactory):
    """View to update Newsimage which is a inline view"""

    model = ClassKeyword
    form_class = ClassKeywordChangeForm
    factory_kwargs = {'extra': 4, 'max_num': 4, 'can_order': False, 'can_delete': True}

class ClassMaterialUpdateInline(InlineFormSetFactory):
    """View to update Newsimage which is a inline view"""

    model = ClassMaterial
    form_class = ClassMaterialChangeForm
    factory_kwargs = {'extra': 4, 'max_num': 4, 'can_order': False, 'can_delete': True}

class ClassCoversUpdateInline(InlineFormSetFactory):
    """View to update Newsimage which is a inline view"""

    model = ClassCovers
    form_class = ClassCoversChangeForm
    factory_kwargs = {'extra': 4, 'max_num': 4, 'can_order': False, 'can_delete': True}

class CreatorClassUpdateView(MyNewFormsetUpdateView):
    """View to update User"""

    model = CreatorClass

    inlines = [ClassKeywordUpdateInline,ClassCoversUpdateInline,ClassMaterialInline ]


    form_class = MyCreatorClassChangeForm
    template_name = "customadmin/classes/creator_class_form.html"
    permission_required = ("customadmin.change_creator_class",)


    def get_success_url(self):
        messages.success(self.request, MSG_UPDATED.format(self.object))
        # opts = self.model._meta
        return reverse("customadmin:creatorclass-list")

class CreatorClassDeleteView(MyDeleteView):
    """View to delete User"""

    model = CreatorClass
    template_name = "customadmin/confirm_delete.html"
    permission_required = ("customadmin.delete_creator_class",)

    def get_success_url(self):
        # opts = self.model._meta
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