from rest_framework import fields, serializers
from ..models import User, UserKeyword, CountryField
from rest_framework.authtoken.models import Token
from customadmin.models import Testimonial, Plan, PlanCover, AdminKeyword
from creator_class.utils import MyStripe
from creator.models import Creator
# from creator.serializers import AdminKeywordSerializer


class CountryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountryField
        fields = ['country_name', 'country_flag']


class AdminKeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminKeyword
        fields = ['id', 'keyword']


class UserKeywordListSerializer(serializers.ModelSerializer):
    keyword = AdminKeywordSerializer()
    class Meta:
        model = AdminKeyword
        fields = ['keyword']


class UserSelectedKeywordSerializer(serializers.ModelSerializer):
    keyword = serializers.CharField(required=True)
    class Meta:
        model = UserKeyword
        fields = ['user', 'keyword']

    def create(self, validated_data):
        user = validated_data.pop('user', None)
        keywords = validated_data.pop('keyword', None)
        keywords = keywords.split(',')
        for keyword in keywords:
            admin_keyword = AdminKeyword.objects.filter(pk=keyword)
            if admin_keyword:
                keyword_exists = UserKeyword.objects.filter(user=user.pk, keyword=keyword)
                if not keyword_exists:
                    UserKeyword.objects.create(keyword=admin_keyword.first(), user=user)
        instance = {}
        instance['user'] = user
        instance['keyword'] = keyword
        return instance


class UserProfileSerializer(serializers.ModelSerializer):
    """
    User Profile serializer
    """
    email = serializers.EmailField()
    token = serializers.SerializerMethodField(read_only=True)
    password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(read_only=True, required=False)
    affiliation_code = serializers.CharField(required=False)
    selected_keywords = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'token', 'password', 'confirm_password','profile_image', 'is_creator', 'affiliation_code', 'selected_keywords']
    
        extra_kwargs = {"password":
                                {"write_only": True}
                            }

    def create(self, validated_data):
        """
        custom 'create' so that password gets hashed!
        """
        password = validated_data.pop('password', None)
        affiliation_code = validated_data.pop('affiliation_code', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()

        if affiliation_code:
            creators = Creator.objects.filter(is_active=True, affiliation_link__contains=affiliation_code)
            if creators:
                instance.affiliated_with = creators[0]
                instance.save()

        # Create Stripe customer ID
        stripe = MyStripe()
        customer = stripe.create_customer(instance)
        instance.customer_id = customer.id
        instance.save()
        return instance


    def get_token(self, obj):
        return f"Token {Token.objects.get_or_create(user=obj)[0]}"

    def get_selected_keywords(self, instance):
        selected_keywords = UserKeyword.objects.filter(user=instance.pk)
        serializer = UserKeywordListSerializer(selected_keywords, many=True)
        return serializer.data


class TestimonialListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = ['id', 'created_at', 'image', 'name', 'email', 'testimonial_text', 'rating']


class PlanListingSerializer(serializers.ModelSerializer):
    plan_covers = serializers.SerializerMethodField()
    class Meta:
        model = Plan
        fields = ['id', 'name', 'plan_amount', 'duration_in_months', 'plan_covers', 'stripe_plan_id', 'paypal_plan_id']

    def get_plan_covers(self, instance):
        plan_covers = PlanCover.objects.filter(plan=instance)
        return [plan_cover.covers for plan_cover in plan_covers]


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """
    User Profile update serializer
    """
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'description', 'profile_image','country_details']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['country'] = CountryListSerializer(instance.country_details).data
        return response


class UserPlanSerializer(serializers.ModelSerializer):
    plan_id = PlanListingSerializer()
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'description', 'profile_image', 'plan_id', 'plan_purchased_at', 'stripe_subscription_id', 'paypal_subscription_id']

