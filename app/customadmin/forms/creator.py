# -*- coding: utf-8 -*-

from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import Group, Permission

from ..utils import filter_perms

from customadmin.utils import Emails
from django.template import loader

from creator.models import Creator, CreatorSkill

from django.contrib.auth.hashers import make_password, check_password

# -----------------------------------------------------------------------------
# Creators
# -----------------------------------------------------------------------------


class MyCreatorCreationForm(forms.ModelForm):
    """Custom UserCreationForm."""

    password=forms.CharField(widget=forms.PasswordInput())
    confirm_password=forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Creator
        fields = [
            "email",
            "username",
            "first_name",
            "last_name",
            "profile_image",
            "description",
            "is_active",
            "is_superuser",
            "is_staff",
            "groups",
            "user_permissions",
            "password",
            "confirm_password",

            "key_skill",
            "instagram_url",
            "linkedin_url",
            "twitter_url",
            "google_url",
            "facebook_url",
        ]

    def __init__(self, *args, **kwargs):
        # self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        print(*args)

    def clean(self):
        cleaned_data = super(MyCreatorCreationForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.is_creator = True
            instance.password = make_password(instance.password)
            instance.save()


        return instance



class MyCreatorChangeForm(forms.ModelForm):
    """Custom UserChangeForm."""
    class Meta:
        model = Creator
        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
            "profile_image",
            "description",
            "is_active",
            "is_superuser",
            "is_staff",

            "key_skill",
            "instagram_url",
            "linkedin_url",
            "twitter_url",
            "google_url",
            "facebook_url",
        )

class CreatorSkillCreationForm(forms.ModelForm):
    """Custom form to create Chat settings"""

    class Meta():
        model = CreatorSkill
        fields = [
            "skill",
            "creator",
        ]

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()

        return instance


class CreatorSkillChangeForm(forms.ModelForm):
    """Custom form to change Chat settings"""

    class Meta():
        model = CreatorSkill

        fields = [
            "skill",
            "creator",
        ]
    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()

        return instance