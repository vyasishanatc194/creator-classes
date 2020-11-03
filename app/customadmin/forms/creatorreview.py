# -*- coding: utf-8 -*-

from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import Group, Permission

from ..utils import filter_perms

from customadmin.utils import Emails
from django.template import loader

from user.models import CreatorReview

from django.contrib.auth.hashers import make_password, check_password

# -----------------------------------------------------------------------------
# Creators
# -----------------------------------------------------------------------------


class MyCreatorReviewCreationForm(forms.ModelForm):
    """Custom UserCreationForm."""


    class Meta:
        model = CreatorReview
        fields = [
            "user",
            "creator",
            "review",
            "rating",
        ]

    def __init__(self, *args, **kwargs):
        # self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        print(*args)

    def clean(self):
        cleaned_data = super(MyCreatorReviewCreationForm, self).clean()
        user = cleaned_data.get("user")
        creator = cleaned_data.get("creator")
        print(creator,".....", user)
        rating = cleaned_data.get("rating")

        if user == creator:
            raise forms.ValidationError(
                "user and creator must be different."
            )
        



    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()


        return instance



class MyCreatorReviewChangeForm(forms.ModelForm):
    """Custom UserChangeForm."""
    class Meta:
        model = CreatorReview
        fields = (
            "user",
            "creator",
            "review",
            "rating",
        )
