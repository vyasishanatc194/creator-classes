from rest_framework import fields, serializers
from ..models import CreatorReview, User


class CreatorReviewSerializer(serializers.ModelSerializer):
    review = serializers.CharField(required=True)
    rating = serializers.FloatField(required=True)
    class Meta:
        model = CreatorReview
        fields = ('id','user', 'creator','review','rating',)

    