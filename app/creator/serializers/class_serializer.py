from rest_framework import fields, serializers
from ..models import Creator, CreatorClass, ClassKeyword, ClassCovers
from user.models import CreatorReview, User, ClassReview
from rest_framework.authtoken.models import Token
from django.db.models import Sum


class AddClassSerializer(serializers.ModelSerializer):
    """
    Add Class serializer
    """
    title = serializers.CharField(required=True)
    class_file = serializers.FileField(required=True)
    thumbnail_file = serializers.FileField(required=True)
    class_keywords = serializers.ListField()
    class_covers = serializers.ListField()

    class Meta:
        model = CreatorClass
        fields = ['id', 'creator', 'title', 'thumbnail_file', 'class_file', 'class_keywords', 'class_covers']

    def create(self, validated_data):
        class_keywords = validated_data.pop('class_keywords', None)
        class_covers = validated_data.pop('class_covers', None)
        creator_class =CreatorClass.objects.create(**validated_data)
        if class_keywords:
            for keyword in class_keywords:
                ClassKeyword.objects.create(keyword=keyword, creator_class=creator_class)

        if class_covers:
            for content in class_covers:
                ClassCovers.objects.create(covers=content, creator_class=creator_class)
        creator_class.class_keywords = [keyword for keyword in class_keywords]
        creator_class.class_covers = [covers for covers in class_covers]
        return creator_class

    def update(self, instance, validated_data):
        class_keywords = validated_data.pop('class_keywords', None)
        class_covers = validated_data.pop('class_covers', None)
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
            instance.save()

        if class_keywords:
            ClassKeyword.objects.filter(creator_class=instance).delete()
            for keyword in class_keywords:
                ClassKeyword.objects.create(keyword=keyword, creator_class=instance)

        if class_covers:
            ClassCovers.objects.filter(creator_class=instance).delete()
            for covers in class_covers:
                ClassCovers.objects.create(covers=covers, creator_class=instance)

        instance.class_keywords=class_keywords
        instance.class_covers=class_covers
        return instance


class ClassListingSerializer(serializers.ModelSerializer):
    """
    CLass listing serializer
    """
    avg_rating = serializers.SerializerMethodField()
    total_rating = serializers.SerializerMethodField()

    class Meta:
        model = CreatorClass
        fields = ['id', 'title', 'thumbnail_file', 'class_file', 'avg_rating', 'total_rating']

    def get_avg_rating(self, instance):
        ratings = ClassReview.objects.filter(creator_class=instance)
        sum_ratings = ratings.aggregate(Sum('rating'))
        if sum_ratings['rating__sum'] and ratings.count():
            return sum_ratings['rating__sum']/ratings.count()
        return 0

    def get_total_rating(self, instance):
        ratings = ClassReview.objects.filter(creator_class=instance).count()
        return ratings
