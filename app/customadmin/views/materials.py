# -*- coding: utf-8 -*-
from customadmin.mixins import HasPermissionsMixin
from customadmin.views.generic import (
    MyCreateView,
    MyDeleteView,
    MyListView,
    MyDetailView,
    MyLoginRequiredView,
    MyUpdateView,
    get_aws_s3_creds
)
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.db.models import Q
from django.template.loader import get_template
from django_datatables_too.mixins import DataTableMixin

from customadmin.forms import MyMaterialCategoryCreationForm, MyMaterialCategoryChangeForm, MyMaterialCreationForm, MyMaterialChangeForm
from django.shortcuts import reverse, render
from creator.models import MaterialCategory, Material

# -----------------------------------------------------------------------------
# Material Category
# -----------------------------------------------------------------------------

class MaterialCategoryListView(MyListView):
    """View for Material Category listing"""

    ordering = ["id"]
    model = MaterialCategory
    queryset = model.objects.all()
    template_name = "customadmin/materials/material_category_list.html"
    permission_required = ("customadmin.view_material_category",)

    def get_queryset(self):
        return self.model.objects.all().exclude(active=False).order_by('-created_at')

class MaterialCategoryCreateView(MyCreateView):
    """View to create Material Category"""

    model = MaterialCategory
    form_class = MyMaterialCategoryCreationForm
    template_name = "customadmin/materials/material_category_form.html"
    permission_required = ("customadmin.add_material_category",)

    def get_success_url(self):
        return reverse("customadmin:materialcategory-list")

class MaterialCategoryUpdateView(MyUpdateView):
    """View to update Material Category"""

    model = MaterialCategory
    form_class = MyMaterialCategoryChangeForm
    template_name = "customadmin/materials/material_category_form.html"
    permission_required = ("customadmin.change_material_category",)

    def get_success_url(self):
        return reverse("customadmin:materialcategory-list")

class MaterialCategoryDeleteView(MyDeleteView):
    """View to delete Material Category"""

    model = MaterialCategory
    template_name = "customadmin/confirm_delete.html"
    permission_required = ("customadmin.delete_material_category",)

    def get_success_url(self):
        return reverse("customadmin:materialcategory-list")

class MaterialCategoryAjaxPagination(DataTableMixin, HasPermissionsMixin, MyLoginRequiredView):
    """Built this before realizing there is
    https://bitbucket.org/pigletto/django-datatables-view."""

    model = MaterialCategory
    queryset = MaterialCategory.objects.all().order_by("created_at")

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

# =================================================================================
# =================================================================================
# =========================      Material        ==================================
# =================================================================================
# =================================================================================

class MaterialDetailView(MyDetailView):
    model = Material
    template_name = "customadmin/materials/material_detail.html"
    permission_required = ("customadmin.view_material_detail",)
    context = {}

    def get(self, request, pk):
        self.context['material_detail'] = Material.objects.filter(pk=pk).first()
        self.context['material_file_url'] = request.build_absolute_uri(self.context['material_detail'].material_file)
        self.context['material_file_url'] = self.context['material_file_url'][:22] + 'media' + self.context['material_file_url'][51:]
        return render(request, self.template_name, self.context)

class MaterialListView(MyListView):
    """View for Material listing"""

    # paginate_by = 25
    ordering = ["id"]
    model = Material
    queryset = model.objects.all()
    template_name = "customadmin/materials/material_list.html"
    permission_required = ("customadmin.view_material",)

    def get_queryset(self):
        return self.model.objects.all().exclude(active=False).order_by('-created_at')

class MaterialCreateView(MyCreateView):
    """View to create Material"""

    model = Material

    form_class = MyMaterialCreationForm
    template_name = "customadmin/materials/material_form.html"
    permission_required = ("customadmin.add_material",)

    def get_context_data(self, *args, **kwargs):
        
        context = super().get_context_data( *args, **kwargs)
        context.update(get_aws_s3_creds())
        context['path'] = 'materials'
        return context

    def get_success_url(self):
        return reverse("customadmin:material-list")

class MaterialUpdateView(MyUpdateView):
    """View to update Material"""

    model = Material
    form_class = MyMaterialChangeForm
    template_name = "customadmin/materials/material_form.html"
    permission_required = ("customadmin.change_material",)
    
    def get_context_data(self, *args, **kwargs):
        
        context = super().get_context_data( *args, **kwargs)
        context.update(get_aws_s3_creds())
        context['path'] = 'materials'
        return context

    def get_success_url(self):
        return reverse("customadmin:material-list")

class MaterialDeleteView(MyDeleteView):
    """View to delete Material"""

    model = Material
    template_name = "customadmin/confirm_delete.html"
    permission_required = ("customadmin.delete_material",)

    def get_success_url(self):
        return reverse("customadmin:material-list")

class MaterialAjaxPagination(DataTableMixin, HasPermissionsMixin, MyLoginRequiredView):
    """Built this before realizing there is
    https://bitbucket.org/pigletto/django-datatables-view."""

    model = Material
    queryset = Material.objects.all().order_by("created_at")

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