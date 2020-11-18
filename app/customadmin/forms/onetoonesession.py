# -*- coding: utf-8 -*-

from django import forms

from creator.models import OneToOneSession, TimeSlot, Creator
from django.utils import timezone
import datetime
# -----------------------------------------------------------------------------
# Creator's OneToOne Sessions
# -----------------------------------------------------------------------------


class OneToOneSessionCreationForm(forms.ModelForm):
    """Custom OneToOneSessionCreationForm."""

    class Meta:
        model = OneToOneSession
        fields = [
            "creator",
            "amount",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['creator'].queryset = Creator.objects.filter(status='ACCEPT')
        self.fields['creator'].required = False

    def clean(self):
        cleaned_data = super(OneToOneSessionCreationForm, self).clean()
        creator = cleaned_data.get("creator")
        amount = cleaned_data.get("amount")

        instance = OneToOneSession.objects.filter(creator=creator).first()
        if instance:
            raise forms.ValidationError(
                "Creator Session Exists."
            )

        if not creator:
            raise forms.ValidationError(
                "Please select creator."
            )
        if float(amount) < 0.0:
            raise forms.ValidationError(
                "Amount must be grater than zero."
            )

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance



class OneToOneSessionChangeForm(forms.ModelForm):
    """Custom OneToOneSessionChangeForm."""
    class Meta:
        model = OneToOneSession
        fields = (
            "creator",
            "amount",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['creator'].queryset = Creator.objects.filter(status='ACCEPT')
        self.fields['creator'].required = False


    def clean(self):
        cleaned_data = super(OneToOneSessionChangeForm, self).clean()
        creator = cleaned_data.get("creator")
        amount = cleaned_data.get("amount")

        if OneToOneSession.objects.filter(creator=creator).exclude(pk=self.instance.id).count() > 0:
            raise forms.ValidationError(
                "Creator Session exists."
            )

        if not creator:
            raise forms.ValidationError(
                "Please select creator."
            )
        if float(amount) < 0.0:
            raise forms.ValidationError(
                "Amount must be grater than zero."
            )

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance

# -----------------------------------------------------------------------------
# Creator's TimeSlots
# -----------------------------------------------------------------------------


class TimeSlotCreationForm(forms.ModelForm):
    """Custom TimeSlotCreationForm."""

    class Meta:
        model = TimeSlot
        fields = [
            "session",
            "slot_datetime",
            "is_booked",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(*args)

    def clean(self):
        cleaned_data = super(TimeSlotCreationForm, self).clean()
        slot_datetime = cleaned_data.get("slot_datetime")
        today_date = timezone.now()
        if today_date > slot_datetime:
            raise forms.ValidationError(
                "Please add valid date and time."
            )

        if not slot_datetime:
            raise forms.ValidationError(
                "Please add slot date time."
            )

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance



class TimeSlotChangeForm(forms.ModelForm):
    """Custom TimeSlotChangeForm."""
    class Meta:
        model = TimeSlot
        fields = (
            "session",
            "slot_datetime",
            "is_booked",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(*args)

    def clean(self):
        cleaned_data = super(TimeSlotChangeForm, self).clean()
        slot_datetime = cleaned_data.get("slot_datetime")
        today_date = timezone.now()
        if today_date > slot_datetime:
            raise forms.ValidationError(
                "Please add valid date and time."
            )

        if not slot_datetime:
            raise forms.ValidationError(
                "Please add slot date time."
            )
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance