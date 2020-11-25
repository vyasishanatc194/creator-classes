# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from user.models import UserCard, User
from ..utils import filter_perms
from itertools import groupby
import re
import datetime
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

# -----------------------------------------------------------------------
# User Card
# -----------------------------------------------------------------------
class UserCardCreationForm(forms.ModelForm):
    """Custom ClassReviewCreationForm."""

    class Meta:
        model = UserCard
        fields = [
            "user",
            "card_number",
            "expiry_month_year",
            "stripe_token",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(is_creator=False).exclude(username='admin')
        self.fields['user'].required = False

    def clean(self):
        cleaned_data = super(UserCardCreationForm, self).clean()
        user = cleaned_data.get("user")
        card_number = cleaned_data.get("card_number")
        expiry_month_year = cleaned_data.get("expiry_month_year")
        stripe_token = cleaned_data.get("stripe_token")

        if not user :
            raise forms.ValidationError(
                "Please select user."
            )
        if not card_number :
            raise forms.ValidationError(
                "Please enter card number."
            )
        if not expiry_month_year :
            raise forms.ValidationError(
                "Please enter card expiry month and year."
            )
        if not stripe_token :
            raise forms.ValidationError(
                "Please enter stripe token."
            )
        card_pattern = '^[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{4}$'
        expiry_pattern = '^[0-9]{2}/[0-9]{4}$'
        number = re.match(card_pattern, card_number)
        expiry = re.match(expiry_pattern, expiry_month_year)
        month_range = expiry_month_year[:2]
        year_range = expiry_month_year[3:]
        now = datetime.datetime.now()
        if not number:
            raise forms.ValidationError(
                "Please enter card number in valid format [0000-0000-0000-0000]."
            )
        if not expiry:
            raise forms.ValidationError(
                "Please enter expiry month year in valid format [00/0000]."
            )
        if int(month_range)<=0 or int(month_range)>=13:
            raise forms.ValidationError(
                "Please enter the valid month."
            )
        if int(year_range)==now.year and int(month_range)<=now.month:
            raise forms.ValidationError(
                "Please enter the year grater or equal to current month."
            )
        if int(year_range)<now.year:
            raise forms.ValidationError(
                "Please enter the year grater or equal to current year."
            )
        instance = UserCard.objects.filter(card_number__iexact=card_number).first()
        if instance:
            raise forms.ValidationError(
                "Card number already exists."
            )

    def save(self, commit=True):
        instance = super().save(commit=False)
        cleaned_data = super(UserCardCreationForm, self).clean()
        card_number = cleaned_data.get("card_number")
        if commit:
            instance.card_number = '****-****-****-' + card_number[15:]
            instance.save()
        return instance

class UserCardChangeForm(forms.ModelForm):
    """Custom ClassReviewChangeForm."""
    class Meta:
        model = UserCard
        fields = (
            "user",
            "card_number",
            "expiry_month_year",
            "stripe_token",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].required = False

    def clean(self):
        cleaned_data = super(UserCardChangeForm, self).clean()
        user = cleaned_data.get("user")
        card_number = cleaned_data.get("card_number")
        expiry_month_year = cleaned_data.get("expiry_month_year")
        stripe_token = cleaned_data.get("stripe_token")

        if not user :
            raise forms.ValidationError(
                "Please select user."
            )
        if not card_number :
            raise forms.ValidationError(
                "Please enter card number."
            )
        if not expiry_month_year :
            raise forms.ValidationError(
                "Please enter card expiry month and year."
            )
        if not stripe_token :
            raise forms.ValidationError(
                "Please enter stripe token."
            )
        expiry_pattern = '^[0-9]{2}/[0-9]{4}$'
        expiry = re.match(expiry_pattern, expiry_month_year)
        month_range = expiry_month_year[:2]
        year_range = expiry_month_year[3:]
        now = datetime.datetime.now()
        if not expiry:
            raise forms.ValidationError(
                "Please enter expiry month year in valid format [00/0000]."
            )
        if int(month_range)<=0 or int(month_range)>=13:
            raise forms.ValidationError(
                "Please enter the valid month."
            )
        if int(year_range)==now.year and int(month_range)<=now.month:
            raise forms.ValidationError(
                "Please enter the year grater or equal to current month."
            )
        if int(year_range)<now.year:
            raise forms.ValidationError(
                "Please enter the year grater or equal to current year."
            )
        if UserCard.objects.filter(card_number__iexact=card_number).exclude(pk=self.instance.id).count() > 0:
            raise forms.ValidationError(
                "Card number already exists."
            )
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance