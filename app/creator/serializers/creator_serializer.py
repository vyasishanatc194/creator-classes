from rest_framework import fields, serializers
from ..models import Creator, CreatorSkill
from user.models import CreatorReview, User
from rest_framework.authtoken.models import Token
from django.db.models import Sum


class CreatorSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreatorSkill
        fields = ['skill']


class CreatorProfileSerializer(serializers.ModelSerializer):
    """
    Creator Profile serializer
    """
    email = serializers.EmailField(read_only=True)
    token = serializers.SerializerMethodField(read_only=True)
    other_skills = serializers.ListField()

    class Meta:
        model = Creator
        fields = ['id', 'email', 'first_name', 'last_name', 'username', 'token', 'profile_image', 'description', 'key_skill', 'other_skills', 'instagram_url', 'linkedin_url', 'twitter_url', 'google_url', 'facebook_url']


    def update(self, instance, validated_data):
        other_skills = validated_data.pop('other_skills', None)
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
            instance.save()

        if other_skills:
            CreatorSkill.objects.filter(creator=instance).delete()
            for skill in other_skills:
                CreatorSkill.objects.create(creator=instance, skill=skill)
        instance.other_skills=other_skills
        return instance


    def get_token(self, obj):
        return f"Token {Token.objects.get_or_create(user=obj)[0]}"


# class UserReviewSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email', 'profile_image']


# class CreatorReviewListingSerializer(serializers.ModelSerializer):
#     """
#     Creator reviews listing serializer
#     """
#     user = UserReviewSerializer()
#     class Meta:
#         model = CreatorReview
#         fields = ['id', 'user', 'review', 'rating']


class CreatorProfileDisplaySerializer(serializers.ModelSerializer):
    """
    Creator Profile display serializer
    """
    email = serializers.EmailField(read_only=True)
    other_skills = serializers.SerializerMethodField()
    avg_rating = serializers.SerializerMethodField()
    total_rating = serializers.SerializerMethodField()

    class Meta:
        model = Creator
        fields = ['id', 'email', 'first_name', 'last_name', 'username', 'profile_image', 'description', 'key_skill', 'other_skills', 'instagram_url', 'linkedin_url', 'twitter_url', 'google_url', 'facebook_url',
        'avg_rating', 'total_rating']

    def get_other_skills(self, instance):
        other_skills = CreatorSkill.objects.filter(creator=instance.pk)
        skills = [skill.skill for skill in other_skills]
        return skills

    def get_avg_rating(self, instance):
        ratings = CreatorReview.objects.filter(creator=instance)
        sum_ratings = ratings.aggregate(Sum('rating'))
        if sum_ratings['rating__sum'] and ratings.count():
            return sum_ratings['rating__sum']/ratings.count()
        return 0

    def get_total_rating(self, instance):
        ratings = CreatorReview.objects.filter(creator=instance).count()
        return ratings


class CreatorListingSerializer(serializers.ModelSerializer):
    """
    Creator listing serializer
    """
    email = serializers.EmailField(read_only=True)
    other_skills = serializers.SerializerMethodField()
    avg_rating = serializers.SerializerMethodField()
    total_rating = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Creator
        fields = ['id', 'email', 'full_name', 'username', 'profile_image', 'key_skill', 'other_skills',
        'avg_rating', 'total_rating']

    def get_other_skills(self, instance):
        other_skills = CreatorSkill.objects.filter(creator=instance.pk)
        skills = [skill.skill for skill in other_skills]
        return skills

    def get_avg_rating(self, instance):
        ratings = CreatorReview.objects.filter(creator=instance)
        sum_ratings = ratings.aggregate(Sum('rating'))
        if sum_ratings['rating__sum'] and ratings.count():
            return sum_ratings['rating__sum']/ratings.count()
        return 0

    def get_total_rating(self, instance):
        ratings = CreatorReview.objects.filter(creator=instance).count()
        return ratings

    def get_full_name(self, instance):
        return f"{instance.first_name} {instance.last_name}"
