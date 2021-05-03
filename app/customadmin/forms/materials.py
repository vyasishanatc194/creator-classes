# -*- coding: utf-8 -*-

from django import forms

from creator.models import MaterialCategory, Material, Creator

# -----------------------------------------------------------------------------
# Material Categories
# -----------------------------------------------------------------------------


class MyMaterialCategoryCreationForm(forms.ModelForm):
    """Custom MaterialCategoryCreationForm."""

    class Meta:
        model = MaterialCategory
        fields = [
            "category_title",
            "category_image",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(MyMaterialCategoryCreationForm, self).clean()
        category_title = cleaned_data.get("category_title")
        category_image = cleaned_data.get("category_image")

        instance = MaterialCategory.objects.filter(category_title__iexact=category_title).first()

        if instance:
            raise forms.ValidationError(
                "Category Title already exists."
            )
        if not category_title:
            raise forms.ValidationError(
                "Please add category title"
            )
        if not category_image:
            raise forms.ValidationError(
                "Please add category image"
            )

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance



class MyMaterialCategoryChangeForm(forms.ModelForm):
    """Custom MaterialCategoryChangeForm."""

    class Meta:
        model = MaterialCategory
        fields = (
            "category_title",
            "category_image",
        )

    def clean(self):
        cleaned_data = super(MyMaterialCategoryChangeForm, self).clean()
        category_title = cleaned_data.get("category_title")
        category_image = cleaned_data.get("category_image")

        if MaterialCategory.objects.filter(category_title__iexact=category_title).exclude(pk=self.instance.id).count() > 0:
            raise forms.ValidationError(
                "Material Category already exists."
            )
        if not category_title:
            raise forms.ValidationError(
                "Please add category title"
            )
        if not category_image:
            raise forms.ValidationError(
                "Please add category image"
            )

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance

# -----------------------------------------------------------------------------
# Materials
# -----------------------------------------------------------------------------

class MyMaterialCreationForm(forms.ModelForm):
    """Custom MaterialCreationForm."""
    
    material_file = forms.CharField(required=False)

    class Meta:
        model = Material
        fields = [
            "creator",
            "material_category",
            "title",
            "thumbnail_file",
            "material_file",
        ]

    def __init__(self, *args, **kwargs):
        # self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.fields['creator'].queryset = Creator.objects.filter(status='ACCEPT')
        self.fields['creator'].required = False
        self.fields['material_category'].required = False

    def clean(self):
        cleaned_data = super(MyMaterialCreationForm, self).clean()
        creator = cleaned_data.get("creator")
        material_category = cleaned_data.get("material_category")
        title = cleaned_data.get("title")
        thumbnail_file = cleaned_data.get("thumbnail_file")
        material_file = cleaned_data.get("material_file")

        instance = Material.objects.filter(title__iexact=title, creator=creator).first()

        if instance:
            raise forms.ValidationError(
                "Enter title present in material list for selected creator.Please add another title."
            )

        if not creator:
            raise forms.ValidationError(
                "Please select creator for material"
            )
        if not material_category:
            raise forms.ValidationError(
                "Please select material category for material"
            )
        if not title:
            raise forms.ValidationError(
                "Please add title for material"
            )
        if not thumbnail_file:
            raise forms.ValidationError(
                "Please add thumbnail file"
            )
        if not material_file:
            raise forms.ValidationError(
                "Please add material file"
            )

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance

class MyMaterialChangeForm(forms.ModelForm):
    """Custom MaterialChangeForm."""
    
    material_file = forms.CharField(required=False)

    class Meta:
        model = Material
        fields = (
            "creator",
            "material_category",
            "title",
            "thumbnail_file",
            "material_file",
        )

    
    def __init__(self, *args, **kwargs):
        # self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.fields['creator'].queryset = Creator.objects.filter(status='ACCEPT')
        self.fields['creator'].required = False
        self.fields['material_category'].required = False

    def clean(self):
        cleaned_data = super(MyMaterialChangeForm, self).clean()
        creator = cleaned_data.get("creator")
        material_category = cleaned_data.get("material_category")
        title = cleaned_data.get("title")
        thumbnail_file = cleaned_data.get("thumbnail_file")
        material_file = cleaned_data.get("material_file")

        if Material.objects.filter(creator=creator, title__iexact=title).exclude(pk=self.instance.id).count() > 0:
            raise forms.ValidationError(
                "Material already exists with this creator."
            )
        if not creator:
            raise forms.ValidationError(
                "Please select creator for material"
            )
        if not material_category:
            raise forms.ValidationError(
                "Please select material category for material"
            )
        if not title:
            raise forms.ValidationError(
                "Please add title for material"
            )
        if not thumbnail_file:
            raise forms.ValidationError(
                "Please add thumbnail file"
            )
        if not material_file:
            raise forms.ValidationError(
                "Please add material file"
            )