# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from ..utils import filter_perms


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
            "password2",

        ]
        labels = {
        "is_staff": "Client Admin",    
        "is_superuser": "TF Admin",
        "groups": "User Role",
        }

    def __init__(self, user, *args, **kwargs):
        # self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.user = user
        print(*args)
        self.fields['username'].required = True
        self.fields['password1'].required = False
        self.fields['password2'].required = False

         # filter out the permissions we don't want the user to see
        if not self.user.is_superuser:
            self.fields["user_permissions"].queryset = filter_perms()
        else:
            # self.fields["user_permissions"].queryset = False
            pass

    def clean(self):
        cleaned_data = super(MyUserCreationForm, self).clean()
        email = cleaned_data.get("email")
        username = cleaned_data.get("username")
        print(username,'........')
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")

        if not email:
            raise forms.ValidationError(
                "Please enter email"
            )
        if not username:
            raise forms.ValidationError(
                "Please enter username"
            )
        if not password1:
            raise forms.ValidationError(
                "Please enter password"
            )
        if not password2:
            raise forms.ValidationError(
                "Please enter confirm password"
            )
        if not first_name:
            raise forms.ValidationError(
                "Please enter first name"
            )
        if not last_name:
            raise forms.ValidationError(
                "Please enter last name"
            )

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
            "is_superuser",
            "is_staff",
        )

    def __init__(self, user, *args, **kwargs):
        # self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.user = user
        print(*args)
        self.fields['username'].required = False

    def clean(self):
        cleaned_data = super(MyUserChangeForm, self).clean()
        username = cleaned_data.get("username")
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")

        if not username:
            raise forms.ValidationError(
                "Please enter username"
            )
        if not first_name:
            raise forms.ValidationError(
                "Please enter first name"
            )
        if not last_name:
            raise forms.ValidationError(
                "Please enter last name"
            )
