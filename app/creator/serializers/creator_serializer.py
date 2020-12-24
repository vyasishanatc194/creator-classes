from rest_framework import fields, serializers
from ..models import Creator, CreatorSkill
from user.models import CreatorReview
from rest_framework.authtoken.models import Token
from django.db.models import Sum
from user.models import User
from user.serializers import CreatorReviewSerializer


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
        fields = ['id', 'email', 'first_name', 'last_name', 'username', 'token', 'profile_image', 'description', 'key_skill', 'other_skills', 'instagram_url', 'linkedin_url', 'twitter_url', 'google_url', 'facebook_url', 'creator_website_url']


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


class CreatorReviewListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    profile_image = serializers.SerializerMethodField('get_profile_image_url')
    class Meta:
        model = CreatorReview
        fields = ['id', 'review', 'rating', 'username', 'first_name', 'last_name', 'profile_image']

    def get_profile_image_url(self, review_class):
        request = self.context.get('request')
        if review_class.user.profile_image:
            profile_image_url = review_class.user.profile_image.url
            return request.build_absolute_uri(profile_image_url)


class CreatorProfileDisplaySerializer(serializers.ModelSerializer):
    """
    Creator Profile display serializer
    """
    email = serializers.EmailField(read_only=True)
    other_skills = serializers.SerializerMethodField()
    total_rating = serializers.SerializerMethodField()
    creator_reviews = serializers.SerializerMethodField()

    class Meta:
        model = Creator
        fields = ['id', 'email', 'first_name', 'last_name', 'username', 'profile_image', 'description', 'key_skill', 'other_skills', 'instagram_url', 'linkedin_url', 'twitter_url', 'google_url', 'facebook_url', 'creator_website_url', 'total_rating', 'creator_reviews']

    def get_other_skills(self, instance):
        other_skills = CreatorSkill.objects.filter(creator=instance.pk)
        skills = [skill.skill for skill in other_skills]
        return skills

    def get_total_rating(self, instance):
        ratings = CreatorReview.objects.filter(creator=instance).count()
        return ratings

    def get_creator_reviews(self, instance):
        reviews = CreatorReview.objects.filter(creator=instance)
        print(reviews)
        serializer = CreatorReviewListSerializer(reviews, many=True, context={"request": self.context.get('request')})
        return serializer.data  


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


class CreatorRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(read_only=True)

    class Meta:
        model = Creator
        fields = ['id', 'email', 'first_name', 'last_name', 'username', 'password', 'confirm_password', 'profile_image']

    def create(self, validated_data):
        """
        custom 'create' so that password gets hashed!
        """
        if 'username' not in validated_data or not validated_data['username']:
            validated_data['username']=validated_data['email'].split('@')[0]
        username_check = User.objects.filter(username=validated_data['username']).distinct()
        if username_check.exists(): 
            return "Username already exists!"
        validated_data['is_active'] = False
        validated_data['is_creator'] = True
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()

        return instance


class CreatorLoginSerializer(serializers.ModelSerializer):
    """
    Creator Login serializer
    """
    email = serializers.EmailField(read_only=True)
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Creator
        fields = ['id', 'email', 'first_name', 'last_name', 'username', 'token', 'profile_image', 'description', 'key_skill']

    def get_token(self, obj):
        return f"Token {Token.objects.get_or_create(user=obj)[0]}"