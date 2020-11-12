from rest_framework import fields, serializers
from ..models import StreamKeyword, StreamCovers, Stream
from customadmin.models import AdminKeyword


class AddStreamSerializer(serializers.ModelSerializer):
    """
    Add Class serializer
    """
    title = serializers.CharField(required=True)
    thumbnail_file = serializers.FileField(required=True)
    sneak_peak_file = serializers.FileField(required=True)
    stream_datetime = serializers.DateTimeField(required=True)
    stream_amount = serializers.FloatField(required=True)
    total_seats = serializers.IntegerField(required=True)
    stream_keywords = serializers.CharField(required=True)
    stream_covers = serializers.CharField(required=True)

    class Meta:
        model = Stream
        fields = ['id', 'creator', 'title', 'thumbnail_file', 'sneak_peak_file', 'stream_datetime', 'stream_amount', 'total_seats', 'stream_keywords', 'stream_covers']

    def create(self, validated_data):
        stream_keywords = validated_data.pop('stream_keywords', None)
        stream_covers = validated_data.pop('stream_covers', None)
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

        stream.stream_keywords = stream_keywords
        stream.stream_covers = stream_covers
        return stream

    def update(self, instance, validated_data):
        stream_keywords = validated_data.pop('stream_keywords', None)
        stream_covers = validated_data.pop('stream_covers', None)
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

        instance.stream_keywords=stream_keywords
        instance.stream_covers=stream_covers
        return instance

