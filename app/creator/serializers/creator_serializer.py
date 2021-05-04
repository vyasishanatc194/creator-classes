from rest_framework import fields, serializers
from ..models import Creator, CreatorSkill, CreatorAffiliation, CreatorTransferredMoney, TimeSlot
from user.models import CreatorReview , User, FavouriteCreator, SessionBooking
from rest_framework.authtoken.models import Token
from django.db.models import Sum
from user.serializers import PlanListingSerializer, CountryListSerializer
import uuid
from django.conf import settings
from customadmin.models import CreatorClassCommission, AvailableTimezone


class TimezoneListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableTimezone
        fields = ['pk', 'tz']


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
        fields = ['id', 'email', 'first_name', 'last_name', 'username', 'token','profile_image', 'description', 'country_details','key_skill', 'other_skills', 'instagram_url', 'youtube_url', 'facebook_url', 'creator_website_url']


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
    is_fav = serializers.SerializerMethodField()
    class Meta:
        model = Creator
        fields = ['id', 'email', 'first_name', 'last_name', 'username', 'profile_image', 'description','country_details','key_skill', 'other_skills', 'instagram_url', 'youtube_url', 'facebook_url', 'creator_website_url', 'total_rating', 'creator_reviews', 'affiliation_link','is_fav']

    def get_other_skills(self, instance):
        other_skills = CreatorSkill.objects.filter(creator=instance.pk)
        skills = [skill.skill for skill in other_skills]
        return skills

    def get_total_rating(self, instance):
        ratings = CreatorReview.objects.filter(creator=instance).count()
        return ratings

    def get_creator_reviews(self, instance):
        reviews = CreatorReview.objects.filter(creator=instance)
        serializer = CreatorReviewListSerializer(reviews, many=True, context={"request": self.context.get('request')})
        return serializer.data

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['country'] = CountryListSerializer(instance.country_details).data
        return response

    def get_is_fav(self, instance):
        flag = False
        if self.context['request'].user.is_authenticated:
            creator = Creator.objects.filter(creator=self.context['request'].user.id)
            if creator:
                flag = False
                return flag
            else:
                fav_creator = FavouriteCreator.objects.filter(user=self.context['request'].user.id, creator=instance)
                if fav_creator:
                    flag = True
                else:
                    flag = False
            return flag
        else:
            return flag


class CreatorListingSerializer(serializers.ModelSerializer):
    """
    Creator listing serializer
    """
    email = serializers.EmailField(read_only=True)
    other_skills = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    is_fav = serializers.SerializerMethodField()
    session = serializers.SerializerMethodField()

    class Meta:
        model = Creator
        fields = ['id', 'email', 'full_name', 'username', 'profile_image', 'key_skill', 'other_skills','is_fav','session']

    def get_other_skills(self, instance):
        other_skills = CreatorSkill.objects.filter(creator=instance.pk)
        skills = [skill.skill for skill in other_skills]
        return skills

    def get_full_name(self, instance):
        return f"{instance.first_name} {instance.last_name}"

    def get_is_fav(self, instance):
        flag = False
        if self.context['request'].user.is_authenticated:
            fav_creator = FavouriteCreator.objects.filter(user=self.context['request'].user.id, creator=instance)
            if fav_creator:
                flag = True
            else:
                flag = False
            return flag
        else:
            return flag

    def get_session(self, instance):
        flag = False
        if self.context['request'].user.is_authenticated:
            session_status = TimeSlot.objects.filter(session__creator=instance)
            if session_status:
                return True
            else:
                return False
        else:
            return flag


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
        instance.affiliation_link = f"{settings.USER_SIGNUP_LINK}{uuid.uuid4()}"
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
        fields = ['id', 'email', 'first_name', 'last_name', 'username', 'token', 'profile_image', 'is_creator', 'description', 'key_skill']

    def get_token(self, obj):
        return f"Token {Token.objects.get_or_create(user=obj)[0]}"


class AffiliatedUserProfileSerializer(serializers.ModelSerializer):
    """
    Affiliated User Profile serializer
    """
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name','username', 'email', 'description', 'profile_image', 'created_at']


class AffiliationRecordSerializer(serializers.ModelSerializer):
    """
    Affiliation record serializer
    """
    user = AffiliatedUserProfileSerializer()
    plan_id = PlanListingSerializer()
    transfer_amount = serializers.SerializerMethodField()
    admin_amount = serializers.SerializerMethodField()

    class Meta:
        model = CreatorAffiliation
        fields = ['id', 'user', 'plan_id', 'amount', 'transfer_amount', 'admin_amount', 'created_at']

    
    def get_admin_amount(self, instance):
        creator_class_commission = CreatorClassCommission.objects.all().first()
        if not creator_class_commission:
            creator_class_commission = CreatorClassCommission()
            creator_class_commission.affiliation_deduction = 10
            creator_class_commission.creator_class_deduction = 10
            creator_class_commission.save()
        return float(float(instance.amount) * creator_class_commission.affiliation_deduction)/100

    def get_transfer_amount(self, instance):
        creator_class_commission = CreatorClassCommission.objects.all().first()
        if not creator_class_commission:
            creator_class_commission = CreatorClassCommission()
            creator_class_commission.affiliation_deduction = 10
            creator_class_commission.creator_class_deduction = 10
            creator_class_commission.save()
        affiliation_deduction=float(float(instance.amount) * creator_class_commission.affiliation_deduction)/100
        return instance.amount - affiliation_deduction


class CreatorTransferredMoneySerializer(serializers.ModelSerializer):
    class Meta:
        model = CreatorTransferredMoney
        fields = '__all__'