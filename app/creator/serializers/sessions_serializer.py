from rest_framework import fields, serializers
from ..models import OneToOneSession, TimeSlot


class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = ['id', 'session', 'slot_datetime']


class OneToOneSessionSerializer(serializers.ModelSerializer):
    """
    Add Sessions serializer
    """
    time_slots = TimeSlotSerializer(many=True)
    class Meta:
        model = OneToOneSession
        fields = ['id', 'creator', 'amount', 'time_slots']

    def create(self, validated_data):
        print("validated_data", validated_data)
        time_slots = validated_data.pop('time_slots', None)
        print("NEW VALIDATED DATA", validated_data)
        session = OneToOneSession.objects.create(**validated_data)
        session_timings = {}
        print("time_slots", time_slots)
        if time_slots:
            print("HERERERER")
            time_slots = time_slots.split(',')
            print(time_slots)
            for slot in time_slots:
                print("inside for loop")
                session_timings.add({"session": session.pk, "slot_datetime": slot})

        print(session_timings)
        # serializer = TimeSlotSerializer(data=session_timings, many=True)
        # if serializer.is_valid():
        #     serializer.save()
        # else:
        #     return serializer.errors

        session.time_slots = session_timings
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
                TimeSlot.objects.create(session=instance, slot_datetime=slot)
        instance.time_slots=time_slots
        return instance