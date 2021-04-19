from rest_framework import fields, serializers
from ..models import StreamKeyword, StreamCovers, Stream
from customadmin.models import AdminKeyword, AvailableTimezone


class AddStreamSerializer(serializers.ModelSerializer):
    """
    Add Class serializer
    """ 
    title = serializers.CharField(required=True)
    thumbnail_file = serializers.FileField(required=True)
    sneak_peak_file = serializers.FileField(required=False)
    stream_datetime = serializers.DateTimeField(required=True)
    tz = serializers.CharField(required=True)
    stream_amount = serializers.FloatField(required=True)
    total_seats = serializers.IntegerField(required=True)
    stream_keywords = serializers.CharField(required=True)
    stream_covers = serializers.CharField(required=True)

    class Meta:
        model = Stream
        fields = ['id', 'creator', 'title', 'thumbnail_file', 'sneak_peak_file', 'stream_datetime', 'tz', 'stream_amount', 'total_seats', 'stream_keywords', 'stream_covers']

    def create(self, validated_data):
        tz = validated_data.pop('tz', None)
        stream_keywords = validated_data.pop('stream_keywords', None)
        stream_covers = validated_data.pop('stream_covers', None)
        if tz:
            selected_tz = AvailableTimezone.objects.filter(pk=tz)
            validated_data['tz'] = selected_tz.first()
        stream =Stream.objects.create(**validated_data)


        if stream_keywords:
            stream_keywords = stream_keywords.split(',')
            for keyword in stream_keywords:
                admin_keyword = AdminKeyword.objects.filter(pk=keyword)
                if admin_keyword:
                    StreamKeyword.objects.create(keyword=admin_keyword[0], stream=stream)

        if stream_covers:
            stream_covers = stream_covers.split(',')
            for content in stream_covers:
                StreamCovers.objects.create(covers=content, stream=stream)

        validated_data['stream_keywords'] = stream_keywords
        validated_data['stream_covers'] = stream_covers
        return validated_data

    def update(self, instance, validated_data):
        stream_keywords = validated_data.pop('stream_keywords', None)
        stream_covers = validated_data.pop('stream_covers', None)
        tz = validated_data.pop('tz', None)
        if tz:
            selected_tz = AvailableTimezone.objects.filter(pk=selected_tz)
            validated_data['tz'] = selected_tz.first()

        for (key, value) in validated_data.items():
            setattr(instance, key, value)
            instance.save()

        if stream_keywords:
            stream_keywords = stream_keywords.split(',')
            StreamKeyword.objects.filter(stream=instance).delete()
            for keyword in stream_keywords:
                admin_keyword = AdminKeyword.objects.filter(pk=keyword)
                if admin_keyword:
                    StreamKeyword.objects.create(keyword=admin_keyword[0], stream=instance)

        if stream_covers:
            stream_covers = stream_covers.split(',')
            StreamCovers.objects.filter(stream=instance).delete()
            for covers in stream_covers:
                StreamCovers.objects.create(covers=covers, stream=instance)

        validated_data['stream_keywords'] = stream_keywords
        validated_data['stream_covers'] = stream_covers
        return validated_data


class MyStreamSerializer(serializers.ModelSerializer):
    """
    Add Class serializer
    """ 
    title = serializers.CharField(required=True)
    thumbnail_file = serializers.FileField(required=True)
    sneak_peak_file = serializers.FileField(required=False)
    tz = serializers.CharField(required=True)
    tz_value = serializers.SerializerMethodField()
    stream_amount = serializers.FloatField(required=True)
    total_seats = serializers.IntegerField(required=True)
    stream_keywords = serializers.SerializerMethodField()
    stream_covers = serializers.SerializerMethodField()
    profile_image = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()

    class Meta:
        model = Stream
        fields = ['id','profile_image','username','first_name','last_name','creator', 'title', 'thumbnail_file', 'sneak_peak_file', 'stream_datetime', 'tz', 'tz_value', 'stream_amount', 'total_seats', 'stream_keywords', 'stream_covers']

    def get_stream_covers(self, instance):
        stream_covers = StreamCovers.objects.filter(stream=instance)
        return [stream_cover.covers for stream_cover in stream_covers]

    def get_stream_keywords(self, instance):
        stream_keywords = StreamKeyword.objects.filter(stream=instance)
        return [stream_keyword.keyword.keyword for stream_keyword in stream_keywords]

    def get_tz_value(self, instance):
        if instance.tz:
            return instance.tz.tz
        return None

    def get_profile_image(self, instance):
        if instance.creator.profile_image:
            return instance.creator.profile_image.url
        return None

    def get_username(self, instance):
        return instance.creator.username

    def get_first_name(self, instance):
        return instance.creator.first_name

    def get_last_name(self, instance):
        return instance.creator.last_name

class UpdateStreamSerializer(serializers.ModelSerializer):
    """
    Add Class serializer
    """ 
    title = serializers.CharField(required=False)
    thumbnail_file = serializers.FileField(required=False)
    sneak_peak_file = serializers.FileField(required=False)
    stream_datetime = serializers.DateTimeField(required=False)
    tz = serializers.CharField(required=False)
    stream_amount = serializers.FloatField(required=False)
    total_seats = serializers.IntegerField(required=False)
    stream_keywords = serializers.CharField(required=False)
    stream_covers = serializers.CharField(required=False)

    class Meta:
        model = Stream
        fields = ['id', 'title', 'thumbnail_file', 'sneak_peak_file', 'stream_datetime', 'tz', 'stream_amount', 'total_seats', 'stream_keywords', 'stream_covers']

    def update(self, instance, validated_data):
        stream_keywords = validated_data.pop('stream_keywords', None)
        stream_covers = validated_data.pop('stream_covers', None)
        tz = validated_data.pop('tz', None)
        if tz:
            selected_tz = AvailableTimezone.objects.filter(pk=tz)
            validated_data['tz'] = selected_tz.first()
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
            instance.save()

        if stream_keywords:
            stream_keywords = stream_keywords.split(',')
            StreamKeyword.objects.filter(stream=instance).delete()
            for keyword in stream_keywords:
                admin_keyword = AdminKeyword.objects.filter(pk=keyword)
                if admin_keyword:
                    StreamKeyword.objects.create(keyword=admin_keyword[0], stream=instance)

        if stream_covers:
            stream_covers = stream_covers.split(',')
            StreamCovers.objects.filter(stream=instance).delete()
            for covers in stream_covers:
                StreamCovers.objects.create(covers=covers, stream=instance)

        validated_data['stream_keywords'] = stream_keywords
        validated_data['stream_covers'] = stream_covers
        return validated_data
