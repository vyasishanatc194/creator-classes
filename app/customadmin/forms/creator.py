# -*- coding: utf-8 -*-

from django import forms

from creator.models import Creator, CreatorSkill

from django.contrib.auth.hashers import make_password, check_password

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