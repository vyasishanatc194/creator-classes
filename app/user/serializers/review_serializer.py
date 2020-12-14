from rest_framework import fields, serializers
from ..models import CreatorReview, ClassReview


class CreatorReviewSerializer(serializers.ModelSerializer):
    review = serializers.CharField(required=True)
    rating = serializers.FloatField(required=False)
    class Meta:
        model = CreatorReview
        fields = ('id','user', 'creator','review','rating',)


class ClassReviewSerializer(serializers.ModelSerializer):
    review = serializers.CharField(required=True)
    rating = serializers.FloatField(required=False)
    class Meta:
        model = ClassReview
        fields = ('id','user', 'creator_class','review','rating',)