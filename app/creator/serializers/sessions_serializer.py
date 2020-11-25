from rest_framework import fields, serializers
from ..models import OneToOneSession, TimeSlot


class TimeSlotSerializer(serializers.ModelSerializer):
    slot_datetime = serializers.DateTimeField(required=True)
    class Meta:
        model = TimeSlot
        fields = ['id', 'session', 'slot_datetime']


class OneToOneSessionSerializer(serializers.ModelSerializer):
    """
    Add Sessions serializer
    """
    time_slots = serializers.CharField(required=True)
    class Meta:
        model = OneToOneSession
        fields = ['id', 'creator', 'amount', 'time_slots']

    def create(self, validated_data):
        time_slots = validated_data.pop('time_slots', None)
        session = OneToOneSession.objects.create(**validated_data)
        if time_slots:
            time_slots = time_slots.split(',')
            for slot in time_slots:
                serializer = TimeSlotSerializer(data={'session': session.pk, 'slot_datetime': slot})
                if serializer.is_valid():
                    serializer.save()
                else:
                    return serializer.errors
        session.time_slots = serializer.data
        return session

    def update(self, instance, validated_data):
        time_slots = validated_data.pop('time_slots', None)
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
            instance.save()

        if time_slots:
            time_slots = time_slots.split(',')
            TimeSlot.objects.filter(session=instance).delete()
            for slot in time_slots:
                serializer = TimeSlotSerializer(data={'session': instance.pk, 'slot_datetime': slot})
                if serializer.is_valid():
                    serializer.save()
                else:
                    return serializer.errors
        instance.time_slots=time_slots
        return instance


class SessionListingSerializer(serializers.ModelSerializer):
    amount = serializers.SerializerMethodField()
    class Meta:
        model = TimeSlot
        fields = ['id', 'session', 'amount', 'slot_datetime', 'is_booked']
    
    def get_amount(self, instance):
        return instance.session.amount        