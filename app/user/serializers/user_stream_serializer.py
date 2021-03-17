from rest_framework import fields, serializers
from creator.models import StreamKeyword, StreamCovers, Stream
from ..models import CreatorReview, FavouriteCreator, StreamBooking
from customadmin.models import AdminKeyword
from ..serializers import CreatorReviewSerializer, CreatorReviewListSerializer
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
    is_booked = serializers.SerializerMethodField()
    available_seats = serializers.SerializerMethodField()
    tz_value = serializers.SerializerMethodField()

    class Meta:
        model = Stream
        fields = ['id', 'creator', 'title', 'thumbnail_file', 'sneak_peak_file', 'stream_datetime', 'tz', 'tz_value', 'stream_amount', 'total_seats', 'stream_keywords', 'stream_covers', 'creator_reviews', 'is_favourite', 'is_booked', 'available_seats']

    def get_stream_keywords(self, instance):
        stream_keywords = StreamKeyword.objects.filter(stream=instance)
        keywords_list = [stream_keyword.keyword for stream_keyword in stream_keywords]
        admin_keywords = AdminKeyword.objects.filter(keyword__in=keywords_list)
        serializer = AdminKeywordSerializer(admin_keywords, many=True)
        return serializer.data

    def get_stream_covers(self, instance):
        stream_covers = StreamCovers.objects.filter(stream=instance)
        return [stream_covers.covers for stream_covers in stream_covers]

    def get_creator_reviews(self, instance):
        reviews  = CreatorReview.objects.filter(creator=instance.creator)
        serializer = CreatorReviewListSerializer(reviews, many=True, context={"request": self.context.get('request')})
        return serializer.data

    def get_is_favourite(self, instance):
        user = self.context['request'].user
        if not user.is_anonymous:
            is_favourite = FavouriteCreator.objects.filter(creator=instance.creator, user=user)
            return True if is_favourite else False
        return False

    def get_is_booked(self, instance):
        user = self.context['request'].user
        if not user.is_anonymous:
            is_booked = StreamBooking.objects.filter(stream=instance.pk, user=user)
            return True if is_booked else False
        return False

    def get_available_seats(self, instance):
        booked_seats = StreamBooking.objects.filter(stream=instance.pk)
        return instance.total_seats - booked_seats.count()

    def get_tz_value(self, instance):
        if instance.tz:
            return instance.tz.tz
        return None




class StreamListingSerializer(serializers.ModelSerializer):
    """
    Stream detail serializer
    """
    stream_keywords = serializers.SerializerMethodField()
    stream_covers = serializers.SerializerMethodField()
    creator = CreatorListingSerializer()
    tz_value = serializers.SerializerMethodField()

    class Meta:
        model = Stream
        fields = ['id', 'creator', 'title', 'thumbnail_file', 'sneak_peak_file', 'stream_datetime', 'tz', 'tz_value', 'stream_amount', 'total_seats', 'stream_keywords', 'stream_covers', 'completed']

    def get_stream_keywords(self, instance):
        stream_keywords = StreamKeyword.objects.filter(stream=instance)
        return [stream_keyword.keyword.keyword for stream_keyword in stream_keywords]

    def get_stream_covers(self, instance):
        stream_covers = StreamCovers.objects.filter(stream=instance)
        return [stream_covers.covers for stream_covers in stream_covers]

    def get_tz_value(self, instance):
        if instance.tz:
            return instance.tz.tz
        return None