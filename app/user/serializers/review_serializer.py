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


class CreatorReviewListSerializer(serializers.ModelSerializer):
    review = serializers.CharField(required=True)
    rating = serializers.FloatField(required=False)
    profile_image = serializers.SerializerMethodField('get_profile_image_url')
    class Meta:
        model = CreatorReview
        fields = ('id','user', 'profile_image', 'creator','review','rating',)

    def get_profile_image_url(self, review_class):
        request = self.context.get('request')
        if review_class.user.profile_image:
            profile_image_url = review_class.user.profile_image.url
            return request.build_absolute_uri(profile_image_url)