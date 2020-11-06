# -*- coding: utf-8 -*-

from django import forms

from creator.models import MaterialCategory, Material

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
        print(*args)

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


# -----------------------------------------------------------------------------
# Materials
# -----------------------------------------------------------------------------

class MyMaterialCreationForm(forms.ModelForm):
    """Custom MaterialCreationForm."""

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
        super().__init__(*args, **kwargs)
        print(*args)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance

class MyMaterialChangeForm(forms.ModelForm):
    """Custom MaterialChangeForm."""
    class Meta:
        model = Material
        fields = (
            "creator",
            "material_category",
            "title",
            "thumbnail_file",
            "material_file",
        )
