# -*- coding: utf-8 -*-

from django import forms

from creator.models import Creator, CreatorSkill

from django.contrib.auth.hashers import make_password

# -----------------------------------------------------------------------------
# Creators
# -----------------------------------------------------------------------------


class MyCreatorCreationForm(forms.ModelForm):
    """Custom CreatorCreationForm."""

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
        super().__init__(*args, **kwargs)
        self.fields['username'].required = False
        self.fields['password'].required = False
        self.fields['confirm_password'].required = False

    def clean(self):
        cleaned_data = super(MyCreatorCreationForm, self).clean()
        email = cleaned_data.get("email")
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
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
        if not password:
            raise forms.ValidationError(
                "Please enter password"
            )
        if not confirm_password:
            raise forms.ValidationError(
                "Please enter confirm_password"
            )
        if not first_name:
            raise forms.ValidationError(
                "Please enter first name"
            )
        if not last_name:
            raise forms.ValidationError(
                "Please enter last name"
            )
        if password != confirm_password:
            raise forms.ValidationError(
                "Password and Confirm_password does not match"
            )

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.is_creator = True
            instance.is_active = False
            instance.password = make_password(instance.password)
            instance.save()
        return instance

class MyCreatorChangeForm(forms.ModelForm):
    """Custom CreatorChangeForm."""
    class Meta:
        model = Creator
        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
            "profile_image",
            "description",
            "status",

            "key_skill",
            "instagram_url",
            "linkedin_url",
            "twitter_url",
            "google_url",
            "facebook_url",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].required = False

    def clean(self):
        cleaned_data = super(MyCreatorChangeForm, self).clean()
        email = cleaned_data.get("email")
        username = cleaned_data.get("username")
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
            if instance.status=='PENDING':
                instance.is_active = False
            if instance.status=='ACCEPT':
                instance.is_active = True
            if instance.status=='REJECT':
                instance.is_active = False
            instance.password = make_password(instance.password)
            instance.save()
        return instance

# -----------------------------------------------------------------------------
# Creator Skills
# -----------------------------------------------------------------------------

class CreatorSkillCreationForm(forms.ModelForm):
    """Custom form to create Creator skills"""

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
    """Custom form to change Creator skills"""

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