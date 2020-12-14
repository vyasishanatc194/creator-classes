from rest_framework import serializers
from ..models import SessionBooking, StreamBooking


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
