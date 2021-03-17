from rest_framework import serializers
from ..models import SessionBooking, StreamBooking, BookedSessionKeywords
from ..serializers import UserProfileUpdateSerializer, StreamListingSerializer
from creator.serializers import AdminKeywordSerializer, SessionListingSerializer, CreatorListingSerializer


class SessionBookingSerializer(serializers.ModelSerializer):
    """Serializes the Card data into JSON"""
    class Meta:
        model = SessionBooking
        fields = (
            "id",
            "user",
            "creator",
            "time_slot",
            "user_card",
        )


class StreamSeatHolderSerializer(serializers.ModelSerializer):
    user = UserProfileUpdateSerializer()
    class Meta:
        model = StreamBooking
        fields = ("id", "user", "created_at")


class SessionSeatHolderSerializer(serializers.ModelSerializer):
    user = UserProfileUpdateSerializer()
    booked_time_slot = serializers.SerializerMethodField()
    tz_value = serializers.SerializerMethodField()
    booked_session_keywords = serializers.SerializerMethodField()
    time_slot_id = serializers.SerializerMethodField()
    class Meta:
        model = SessionBooking
        fields = ("id", "user", "created_at", 'time_slot_id', 'booked_time_slot', 'tz_value', 'description', 'booked_session_keywords')

    def get_booked_time_slot(self, instance):
        return instance.time_slot.slot_datetime

    def get_time_slot_id(self, instance):
        return instance.time_slot.pk

    def get_booked_session_keywords(self, instance):
        booked_keywords = BookedSessionKeywords.objects.filter(session=instance)
        serializer = AdminKeywordSerializer(booked_keywords, many=True)
        return serializer.data

    def get_tz_value(self, instance):
        if instance.time_slot:
            return instance.time_slot.tz.tz
        return None



class UserBookedStreamListingSerializer(serializers.ModelSerializer):
    stream = StreamListingSerializer()
    class Meta:
        model = StreamBooking
        fields = ("id", "created_at", 'stream')


class UserBookedSessionListingSerializer(serializers.ModelSerializer):
    time_slot = SessionListingSerializer()
    creator = CreatorListingSerializer()
    class Meta:
        model = StreamBooking
        fields = ("id", "created_at", "creator", 'time_slot')