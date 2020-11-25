# -*- coding: utf-8 -*-

from django import forms

from creator.models import Stream, StreamKeyword, StreamCovers, Creator
from django.utils import timezone
# -----------------------------------------------------------------------------
# Creator Streams
# -----------------------------------------------------------------------------

class StreamCreationForm(forms.ModelForm):
    """Custom CreatorCreationForm."""

    class Meta:
        model = Stream
        fields = [
            "creator",
            "title",
            "thumbnail_file",
            "sneak_peak_file",
            "stream_datetime",
            "stream_amount",
            "total_seats",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['creator'].queryset = Creator.objects.filter(status='ACCEPT')
        self.fields['creator'].required = False

    def clean(self):
        cleaned_data = super(StreamCreationForm, self).clean()
        creator = cleaned_data.get("creator")
        title = cleaned_data.get("title")
        thumbnail_file = cleaned_data.get("thumbnail_file")
        sneak_peak_file = cleaned_data.get("sneak_peak_file")
        stream_datetime = cleaned_data.get("stream_datetime")
        stream_amount = cleaned_data.get("stream_amount")
        total_seats = cleaned_data.get("total_seats")
        today_date = timezone.now()

        if not creator :
            raise forms.ValidationError(
                "Please select creator."
            )
        if not title :
            raise forms.ValidationError(
                "Please add class title."
            )
        if not thumbnail_file :
            raise forms.ValidationError(
                "Please add thumbnail file for stream."
            )
        if not sneak_peak_file :
            raise forms.ValidationError(
                "Please add Sneak Peak file for stream."
            )
        if today_date > stream_datetime:
            raise forms.ValidationError(
                "Please add valid date and time."
            )
        if stream_amount < 0.0 :
            raise forms.ValidationError(
                "Stream amount must be grater than 0."
            )
        if total_seats < 0.0 :
            raise forms.ValidationError(
                "Stream total seats must be grater than 0."
            )

    def save(self, commit=True):
        instance = super().save()
        if commit:
            instance.save()
        return instance



class StreamChangeForm(forms.ModelForm):
    """Custom CreatorChangeForm."""

    class Meta:
        model = Stream
        fields = (
            "creator",
            "title",
            "thumbnail_file",
            "sneak_peak_file",        
            "stream_datetime",        
            "stream_amount",        
            "total_seats",  
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['creator'].queryset = Creator.objects.filter(status='ACCEPT')
        self.fields['creator'].required = False

    def clean(self):
        cleaned_data = super(StreamChangeForm, self).clean()
        creator = cleaned_data.get("creator")
        title = cleaned_data.get("title")
        thumbnail_file = cleaned_data.get("thumbnail_file")
        sneak_peak_file = cleaned_data.get("sneak_peak_file")
        stream_datetime = cleaned_data.get("stream_datetime")
        stream_amount = cleaned_data.get("stream_amount")
        total_seats = cleaned_data.get("total_seats")

        today_date = timezone.now()

        if not creator :
            raise forms.ValidationError(
                "Please select creator."
            )
        if not title :
            raise forms.ValidationError(
                "Please add class title."
            )
        if not thumbnail_file :
            raise forms.ValidationError(
                "Please add thumbnail file for stream."
            )
        if not sneak_peak_file :
            raise forms.ValidationError(
                "Please add Sneak Peak file for stream."
            )
        if today_date > stream_datetime:
            raise forms.ValidationError(
                "Please add valid date and time."
            )
        if stream_amount < 0.0 :
            raise forms.ValidationError(
                "Stream amount must be grater than 0."
            )
        if total_seats < 0.0 :
            raise forms.ValidationError(
                "Stream total seats must be grater than 0."
            )

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()

        return instance

# -----------------------------------------------------------------------------
# Stream Keywords
# -----------------------------------------------------------------------------

class StreamKeywordCreationForm(forms.ModelForm):
    """Custom form to create Class Keyword"""

    class Meta():
        model = StreamKeyword
        fields = [
            "keyword",
            "stream",
        ]

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()

        return instance


class StreamKeywordChangeForm(forms.ModelForm):
    """Custom form to change Class Keyword"""

    class Meta():
        model = StreamKeyword

        fields = [
            "keyword",
            "stream",
        ]

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()

        return instance

# -----------------------------------------------------------------------------
# Stream Covers
# -----------------------------------------------------------------------------

class StreamCoversCreationForm(forms.ModelForm):
    """Custom form to create Class Covers"""

    class Meta():
        model = StreamCovers
        fields = [
            "covers",
            "stream",
        ]

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()

        return instance


class StreamCoversChangeForm(forms.ModelForm):
    """Custom form to change Class Covers"""

    class Meta():
        model = StreamCovers

        fields = [
            "covers",
            "stream",
        ]
    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()

        return instance