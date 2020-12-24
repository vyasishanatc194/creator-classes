# -*- coding: utf-8 -*-

from django import forms

from user.models import SessionBooking, StreamBooking, User
from creator.models import Creator, TimeSlot, Stream
# -----------------------------------------------------------------------------
# Session Booking
# -----------------------------------------------------------------------------

class SessionBookingCreationForm(forms.ModelForm):
    """Custom CreatorCreationForm."""

    class Meta:
        model = SessionBooking
        fields = [
            "user",
            "creator",
            "time_slot",   
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(is_creator=False).exclude(username='admin')
        self.fields['creator'].queryset = Creator.objects.filter(status='ACCEPT')
        self.fields['user'].required = False
        self.fields['creator'].required = False
        self.fields['time_slot'].required = False

    def clean(self):
        cleaned_data = super(SessionBookingCreationForm, self).clean()
        user = cleaned_data.get("user")
        creator = cleaned_data.get("creator")
        time_slot = cleaned_data.get("time_slot")
        instance = SessionBooking.objects.filter(user=user, creator=creator,time_slot=time_slot).first()
        if instance:
            raise forms.ValidationError(
                "Session Booking already exists with selected user, creator and Time Slot."
            )

        if not user :
            raise forms.ValidationError(
                "Please select user."
            )
        if not creator :
            raise forms.ValidationError(
                "Please select creator."
            )
        if not time_slot :
            raise forms.ValidationError(
                "Please select time slot."
            )

    def save(self, commit=True):
        instance = super().save()
        if commit:
            slot_obj = TimeSlot.objects.filter(slot_datetime=instance.time_slot.slot_datetime).first()
            slot_obj.is_booked = True
            slot_obj.save()
            instance.save()
        return instance



class SessionBookingChangeForm(forms.ModelForm):
    """Custom CreatorChangeForm."""

    class Meta:
        model = SessionBooking
        fields = (
            "user",
            "creator",
            "time_slot", 
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(is_creator=False).exclude(username='admin')
        self.fields['creator'].queryset = Creator.objects.filter(status='ACCEPT')
        self.fields['user'].required = False
        self.fields['creator'].required = False
        self.fields['time_slot'].required = False

    def clean(self):
        cleaned_data = super(SessionBookingChangeForm, self).clean()
        user = cleaned_data.get("user")
        creator = cleaned_data.get("creator")
        time_slot = cleaned_data.get("time_slot")
        if SessionBooking.objects.filter(user=user, creator=creator, time_slot=time_slot).exclude(pk=self.instance.id).count() > 0:
            raise forms.ValidationError(
                "Session Booking already exists with selected user, creator and Time Slot."
            )

        if not user :
            raise forms.ValidationError(
                "Please select user."
            )
        if not creator :
            raise forms.ValidationError(
                "Please select creator."
            )
        if not time_slot :
            raise forms.ValidationError(
                "Please select time slot."
            )

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            slot_obj = TimeSlot.objects.filter(slot_datetime=instance.time_slot.slot_datetime).first()
            slot_obj.is_booked = True
            slot_obj.save()
            instance.save()

        return instance

# -----------------------------------------------------------------------------
# Stream Booking
# -----------------------------------------------------------------------------

class StreamBookingCreationForm(forms.ModelForm):
    """Custom CreatorCreationForm."""

    class Meta:
        model = StreamBooking
        fields = [
            "user",
            "stream",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(is_creator=False).exclude(username='admin')
        self.fields['user'].required = False
        self.fields['stream'].required = False

    def clean(self):
        cleaned_data = super(StreamBookingCreationForm, self).clean()
        user = cleaned_data.get("user")
        stream = cleaned_data.get("stream")

        stream_obj = Stream.objects.filter(creator=stream.creator).first()
        stream_count = StreamBooking.objects.filter(stream=stream).count()
        instance = StreamBooking.objects.filter(user=user, stream=stream).first()
        if instance:
            raise forms.ValidationError(
                "Stream Booking already exists with selected user and stream."
            )
        if not (stream_count+1) <= stream_obj.total_seats:
            raise forms.ValidationError(
                "Stream Booking Seats Full."
            )
        if not user :
            raise forms.ValidationError(
                "Please select user."
            )
        if not stream :
            raise forms.ValidationError(
                "Please select stream."
            )
        if not user_card :
            raise forms.ValidationError(
                "Please select user card."
            )

    def save(self, commit=True):
        instance = super().save()
        if commit:
            instance.save()
        return instance



class StreamBookingChangeForm(forms.ModelForm):
    """Custom CreatorChangeForm."""

    class Meta:
        model = StreamBooking
        fields = (
            "user",
            "stream",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(is_creator=False).exclude(username='admin')
        self.fields['user'].required = False
        self.fields['stream'].required = False

    def clean(self):
        cleaned_data = super(StreamBookingChangeForm, self).clean()
        user = cleaned_data.get("user")
        stream = cleaned_data.get("stream")
        if StreamBooking.objects.filter(user=user, stream=stream).exclude(pk=self.instance.id).count() > 0:
            raise forms.ValidationError(
                "Stream Booking already exists with selected user and stream."
            )

        if not user :
            raise forms.ValidationError(
                "Please select user."
            )
        if not stream :
            raise forms.ValidationError(
                "Please select stream."
            )
        if not user_card :
            raise forms.ValidationError(
                "Please select user card."
            )

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()

        return instance
