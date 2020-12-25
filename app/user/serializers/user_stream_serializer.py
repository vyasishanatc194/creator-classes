from rest_framework import fields, serializers
from creator.models import StreamKeyword, StreamCovers, Stream
from ..models import CreatorReview, FavouriteCreator
from customadmin.models import AdminKeyword
from ..serializers import CreatorReviewSerializer
from creator.serializers import CreatorListingSerializer, AdminKeywordSerializer


class StreamDetailSerializer(serializers.ModelSerializer):
    """
    Stream detail serializer
    """
    stream_keywords = serializers.SerializerMethodField()
    stream_covers = serializers.SerializerMethodField()
    creator = CreatorListingSerializer()
    creator_reviews = serializers.SerializerMethodField()
    is_favourite = serializers.SerializerMethodField()

    class Meta:
        model = Stream
        fields = ['id', 'creator', 'title', 'thumbnail_file', 'sneak_peak_file', 'stream_datetime', 'stream_amount', 'total_seats', 'stream_keywords', 'stream_covers', 'creator_reviews', 'is_favourite']

    def get_stream_keywords(self, instance):
        stream_keywords = StreamKeyword.objects.filter(stream=instance)
        serializer = AdminKeywordSerializer(stream_keywords, many=True)
        return serializer.data

    def get_stream_covers(self, instance):
        stream_covers = StreamCovers.objects.filter(stream=instance)
        return [stream_covers.covers for stream_covers in stream_covers]

    def get_creator_reviews(self, instance):
        reviews  = CreatorReview.objects.filter(creator=instance.creator)
        serializer = CreatorReviewSerializer(reviews, many=True, context={"request": self.context.get('request')})
        return serializer.data

    def get_is_favourite(self, instance):
        user = self.context['request'].user
        if not user.is_anonymous:
            is_favourite = FavouriteCreator.objects.filter(creator=instance.creator, user=user)
            return True if is_favourite else False
        return False


class StreamListingSerializer(serializers.ModelSerializer):
    """
    Stream detail serializer
    """
    stream_keywords = serializers.SerializerMethodField()
    stream_covers = serializers.SerializerMethodField()
    creator = CreatorListingSerializer()

    class Meta:
        model = Stream
        fields = ['id', 'creator', 'title', 'thumbnail_file', 'sneak_peak_file', 'stream_datetime', 'stream_amount', 'total_seats', 'stream_keywords', 'stream_covers']

    def get_stream_keywords(self, instance):
        stream_keywords = StreamKeyword.objects.filter(stream=instance)
        return [stream_keyword.keyword.keyword for stream_keyword in stream_keywords]

    def get_stream_covers(self, instance):
        stream_covers = StreamCovers.objects.filter(stream=instance)
        return [stream_covers.covers for stream_covers in stream_covers]