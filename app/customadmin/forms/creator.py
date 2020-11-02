# -*- coding: utf-8 -*-

from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import Group, Permission

from ..utils import filter_perms

from customadmin.utils import Emails
from django.template import loader

from creator.models import Creator

# -----------------------------------------------------------------------------
# Creators
# -----------------------------------------------------------------------------


class MyCreatorCreationForm(forms.ModelForm):
    """Custom UserCreationForm."""

    class Meta:
        model = Creator
        fields = [
            "key_skill",
            "instagram_url",
            "linkedin_url",
            "linkedin_url",
            "twitter_url",
            "google_url",
            "facebook_url",
        ]

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()

        return instance


class MyCreatorChangeForm(forms.ModelForm):
    """Custom UserChangeForm."""

    class Meta:
        model = Creator
        fields = (
            "key_skill",
            "instagram_url",
            "linkedin_url",
            "linkedin_url",
            "twitter_url",
            "google_url",
            "facebook_url",
        )