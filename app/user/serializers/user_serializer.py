from rest_framework import fields, serializers
from ..models import User
from rest_framework.authtoken.models import Token
from customadmin.models import Testimonial, Plan, PlanCover
from creator_class.utils import MyStripe
from creator.models import Creator


class UserProfileSerializer(serializers.ModelSerializer):
    """
    User Profile serializer
    """
    email = serializers.EmailField()
    token = serializers.SerializerMethodField(read_only=True)
    password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(read_only=True, required=False)
    affiliation_code = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'token', 'password', 'confirm_password', 'profile_image', 'is_creator', 'affiliation_code']
    
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


class TestimonialListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = ['id', 'created_at', 'image', 'name', 'email', 'testimonial_text', 'rating']


class PlanListingSerializer(serializers.ModelSerializer):
    plan_covers = serializers.SerializerMethodField()
    class Meta:
        model = Plan
        fields = ['id', 'name', 'plan_amount', 'duration_in_months', 'plan_covers']

    def get_plan_covers(self, instance):
        plan_covers = PlanCover.objects.filter(plan=instance)
        return [plan_cover.covers for plan_cover in plan_covers]


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """
    User Profile update serializer
    """
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'description', 'profile_image']


class UserPlanSerializer(serializers.ModelSerializer):
    plan_id = PlanListingSerializer()
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'description', 'profile_image', 'plan_id', 'plan_purchased_at']