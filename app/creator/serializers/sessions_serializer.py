from rest_framework import fields, serializers
from ..models import Creator, OneToOneSession, TimeSlot
from user.models import User, ClassReview, FavouriteClass
from django.db.models import Sum
from customadmin.models import AdminKeyword
from . import CreatorListingSerializer


class OneToOneSessionSerializer(serializers.ModelSerializer):
    """
    Add Sessions serializer
    """
    time_slots = serializers.CharField(required=True)

    class Meta:
        model = CreatorClass
        fields = ['id', 'creator', 'amount', 'time_slots']

    def create(self, validated_data):
        time_slots = validated_data.pop('time_slots', None)
        session = OneToOneSession.objects.create(**validated_data)
        if time_slots:
            time_slots = time_slots.split(',')
            for slot in time_slots:
                TimeSlot.objects.create(session=session, slot_datetime=slot)

        session.time_slots = time_slots
        return session