# -*- coding: utf-8 -*-

from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import Group, Permission

from ..utils import filter_perms

from customadmin.utils import Emails
from django.template import loader

# -----------------------------------------------------------------------------
# Users
# -----------------------------------------------------------------------------


class MyUserCreationForm(UserCreationForm):
    """Custom UserCreationForm."""

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
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
            "password1",

        ]

    def __init__(self, user, *args, **kwargs):
        # self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.user = user
        print(*args)

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()

        return instance


class MyUserChangeForm(UserChangeForm):
    """Custom UserChangeForm."""

    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
            "profile_image",
            "description",
            "is_active",
            
        )

    def __init__(self, user, *args, **kwargs):
        # self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.user = user

        # filter out the permissions we don't want the user to see
        if not self.user.is_superuser:
            self.fields["user_permissions"].queryset = filter_perms()
        else:
            # self.fields["user_permissions"].queryset = False
            pass

    # def save(self, commit=True):
    #     instance = super().save(commit)
    #     return instance
