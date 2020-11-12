from rest_framework import fields, serializers
from ..models import FavouriteCreator, FavouriteClass, ClassReview
from creator.models import CreatorClass
from django.db.models import Sum
from creator.serializers import CreatorListingSerializer


class FavouriteCreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavouriteCreator
        fields = ('id','user', 'creator',)


class FavouriteClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavouriteClass
        fields = ('id','user', 'creator_class',)


class ClassSerializer(serializers.ModelSerializer):
    """
    favourite Class listing serializer
    """
    avg_rating = serializers.SerializerMethodField()
    total_rating = serializers.SerializerMethodField()
    creator = serializers.SerializerMethodField()

    class Meta:
        model = CreatorClass
        fields = ['id', 'creator', 'title', 'thumbnail_file', 'class_file', 'avg_rating', 'total_rating']

    def get_avg_rating(self, instance):
        ratings = ClassReview.objects.filter(creator_class=instance)
        sum_ratings = ratings.aggregate(Sum('rating'))
        if sum_ratings['rating__sum'] and ratings.count():
            return sum_ratings['rating__sum']/ratings.count()
        return 0

    def get_total_rating(self, instance):
        ratings = ClassReview.objects.filter(creator_class=instance).count()
        return ratings

    def get_creator(self, instance):
        return f"{instance.creator.first_name} {instance.creator.last_name}"


class FavouriteClassListSerializer(serializers.ModelSerializer):
    creator_class = ClassSerializer()
    class Meta:
        model = FavouriteClass
        fields = ('id','user', 'creator_class',)


class FavouriteCreatorListSerializer(serializers.ModelSerializer):
    creator = CreatorListingSerializer()
    class Meta:
        model = FavouriteClass
        fields = ('id','user', 'creator',)