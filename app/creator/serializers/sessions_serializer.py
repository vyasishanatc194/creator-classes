from rest_framework import fields, serializers
from ..models import OneToOneSession, TimeSlot
from ..serializers import CreatorListingSerializer


class TimeSlotSerializer(serializers.ModelSerializer):
    slot_datetime = serializers.DateTimeField(required=True)
    tz = serializers.DateTimeField(required=True)
    class Meta:
        model = TimeSlot
        fields = ['id', 'session', 'slot_datetime', 'tz']


class OneToOneSessionSerializer(serializers.ModelSerializer):
    """
    Add Sessions serializer
    """
    time_slots = serializers.CharField(required=True)
    tz = serializers.CharField(required=True)
    class Meta:
        model = OneToOneSession
        fields = ['id', 'creator', 'amount', 'time_slots', 'tz']

    def create(self, validated_data):
        time_slots = validated_data.pop('time_slots', None)
        tz = validated_data.pop('tz', None)
        session = OneToOneSession.objects.create(**validated_data)
        if tz:
            tz_value = AvailableTimezone.objects.filter(pk=tz)
        if time_slots:
            time_slots = time_slots.split(',')
            for slot in time_slots:
                serializer = TimeSlotSerializer(data={'session': session.pk, 'slot_datetime': slot, 'tz': tz_value.first()})
                if serializer.is_valid():
                    serializer.save()
                else:
                    return serializer.errors
        session.time_slots = serializer.data
        return session

    def update(self, instance, validated_data):
        time_slots = validated_data.pop('time_slots', None)
        tz = validated_data.pop('tz', None)
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
            instance.save()

        tz_value = AvailableTimezone.objects.filter(pk=tz)
            
        if time_slots:
            time_slots = time_slots.split(',')
            TimeSlot.objects.filter(session=instance).delete()
            for slot in time_slots:
                serializer = TimeSlotSerializer(data={'session': instance.pk, 'slot_datetime': slot, 'tz': tz_value.first()})
                if serializer.is_valid():
                    serializer.save()
                else:
                    return serializer.errors
        instance.time_slots=time_slots
        return instance


class SessionListingSerializer(serializers.ModelSerializer):
    amount = serializers.SerializerMethodField()
    tz_value = serializers.SerializerMethodField()
    class Meta:
        model = TimeSlot
        fields = ['id', 'session', 'amount', 'slot_datetime', 'tz', 'tz_value', 'is_booked']
    
    def get_amount(self, instance):
        return instance.session.amount

    def get_tz_value(self, instance):
        if instance.tz:
            return instance.tz.tz
        return None


class TimeSlotsListingSerializer(serializers.ModelSerializer):
    # amount = serializers.SerializerMethodField()
    tz_value = serializers.SerializerMethodField()
    class Meta:
        model = TimeSlot
        fields = ['id', 'session', 'slot_datetime', 'is_booked' , 'tz', 'tz_value']
    
    # def get_amount(self, instance):
    #     return instance.session.amount
    def get_amount(self, instance):
        return instance.tz.tz


class OneToOneSessionListingSerializer(serializers.ModelSerializer):
    creator = CreatorListingSerializer()
    class Meta:
        model = OneToOneSession
        fields = ['id', 'creator', 'amount']