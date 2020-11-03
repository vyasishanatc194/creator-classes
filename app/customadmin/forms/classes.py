# -*- coding: utf-8 -*-

from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import Group, Permission

from ..utils import filter_perms

from customadmin.utils import Emails
from django.template import loader

from creator.models import CreatorClass, ClassKeyword, ClassCovers

from django.contrib.auth.hashers import make_password, check_password

# -----------------------------------------------------------------------------
# Creators
# -----------------------------------------------------------------------------


class MyCreatorClassCreationForm(forms.ModelForm):
    """Custom UserCreationForm."""

    class Meta:
        model = CreatorClass
        fields = [
            "creator",
            "title",
            "thumbnail_file",
            "class_file",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(*args)

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()
        return instance



class MyCreatorClassChangeForm(forms.ModelForm):
    """Custom UserChangeForm."""
    class Meta:
        model = CreatorClass
        fields = (
            "creator",
            "title",
            "thumbnail_file",
            "class_file",
        )

class ClassKeywordCreationForm(forms.ModelForm):
    """Custom form to create Chat settings"""

    class Meta():
        model = ClassKeyword
        fields = [
            "keyword",
            "creator_class",
        ]

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()

        return instance


class ClassKeywordChangeForm(forms.ModelForm):
    """Custom form to change Chat settings"""

    class Meta():
        model = ClassKeyword

        fields = [
            "keyword",
            "creator_class",
        ]

class ClassCoversCreationForm(forms.ModelForm):
    """Custom form to create Chat settings"""

    class Meta():
        model = ClassCovers
        fields = [
            "covers",
            "creator_class",
        ]

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()

        return instance


class ClassCoversChangeForm(forms.ModelForm):
    """Custom form to change Chat settings"""

    class Meta():
        model = ClassCovers

        fields = [
            "covers",
            "creator_class",
        ]