from rest_framework.views import APIView
from ..serializers import UserProfileSerializer, TestimonialListingSerializer, PlanListingSerializer, UserProfileUpdateSerializer, TransactionDetailSerializer, UserPlanSerializer
from ..models import User, TransactionDetail
from creator.models import CreatorAffiliation
from creator_class.helpers import custom_response, serialized_response, get_object, send_email
from rest_framework import status, parsers, renderers
from django.contrib.auth import authenticate, login, logout
from creator_class.permissions import IsAccountOwner, IsUser

from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView

from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter
from rest_auth.social_serializers import TwitterLoginSerializer
from rest_auth.registration.serializers import SocialLoginSerializer

from google.views import GoogleOAuth2Adapter
from rest_framework import generics
from customadmin.models import Testimonial, Plan
from creator_class.utils import MyStripe, create_card_object, create_customer_id, create_charge_object
from datetime import datetime
from dateutil.relativedelta import relativedelta
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.conf import settings
import datetime as datetime_obj
import pytz
import uuid
utc = pytz.UTC




class SignUpApiView(APIView):
    """
    User Sign up view
    """
    serializer_class = UserProfileSerializer

    def post(self, request, *args, **kwargs):
        if request.data['email']:
            email_check = User.objects.filter(email=request.data['email']).distinct()
            if email_check.exists():
                message = "Email already exists!"
                return custom_response(True, status.HTTP_400_BAD_REQUEST, message)

            if 'username' not in request.data or not request.data['username']:
                request.data['username']=request.data['email'].split('@')[0]
            
            username_check = User.objects.filter(username=request.data['username']).distinct()
            if username_check.exists():
                message = "Username already exists!"
                return custom_response(True, status.HTTP_400_BAD_REQUEST, message)

            message = "Account created successfully!"
            serializer = self.serializer_class(data=request.data, context={'request': request})
            response_status, result, message = serialized_response(serializer, message)
            status_code = status.HTTP_201_CREATED if response_status else status.HTTP_400_BAD_REQUEST
            # TODO Email
            return custom_response(response_status, status_code, message, result)
        else:
            return custom_response(False, status.HTTP_400_BAD_REQUEST, "Email is required")



class LoginAPIView(APIView):
    """
    User Login View
    """
    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
        parsers.JSONParser,
    )
    renderer_classes = (renderers.JSONRenderer,)

    def post(self, request, format=None):
        email_or_username = request.data.get("email_or_username", None)
        password = request.data.get("password", None)

        account = authenticate(email=email_or_username, password=password)
        if not account:
            user = User.objects.filter(username=email_or_username)
            if user:
                account = authenticate(email=user[0].email, password=password)
        
        if account is not None:
            login(request, account)
            serializer = UserProfileSerializer(account, context={'request':request})
            return custom_response(True, status.HTTP_200_OK, "Login Successful!", serializer.data)
        else:
            message = "Email/password combination invalid"
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)


class LogoutAPIView(APIView):
    """
    User Logout View
    """
    permission_classes = (IsAccountOwner,)

    def post(self, request, format=None):
        request.user.auth_token.delete()
        logout(request)
        message = "Logout successful!"
        return custom_response(True, status.HTTP_200_OK, message)


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    serializer_class = SocialLoginSerializer

# google_login = GoogleLogin.as_view()

class TestimonialsListingAPIView(generics.ListCreateAPIView):
    queryset = Testimonial.objects.filter(active=True)
    serializer_class = TestimonialListingSerializer


class PlansListingAPIView(generics.ListCreateAPIView):
    serializer_class = PlanListingSerializer
    def get(self, request):
        plans = Plan.objects.filter(active=True)
        serializer = self.serializer_class(plans, many=True, context={"request": request})
        message = "Plans fetched successfully!"
        return custom_response(True, status.HTTP_200_OK, message, serializer.data)


class UserProfileAPIView(APIView):
    """
    User Profile view
    """
    serializer_class = UserProfileUpdateSerializer
    permission_classes = (IsAccountOwner,)

    def put(self, request, *args, **kwargs):
        user_profile = get_object(User, request.user.pk)
        if not user_profile:
            message = "User not found!"
            return custom_response(True, status.HTTP_200_OK, message)
        message = "Profile updated successfully!"
        serializer = self.serializer_class(user_profile, data=request.data, partial=True, context={"request": request})
        response_status, result, message = serialized_response(serializer, message)
        status_code = status.HTTP_200_OK if response_status else status.HTTP_400_BAD_REQUEST
        return custom_response(response_status, status_code, message, result)

    def get(self, request):
        user_profile = get_object(User, request.user.pk)
        if not user_profile:
            message = "Requested account details not found!"
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)
        serializer = self.serializer_class(user_profile, context={"request": request})
        message = "User Details fetched Successfully!"
        return custom_response(True, status.HTTP_200_OK, message, serializer.data)


class PlanPurchaseAPIView(APIView):
    """
    API View to purchase plan
    """
    permission_classes = (IsAccountOwner, IsUser)

    def post(self, request, format=None):
        """POST method to create the data"""
        try:
            if "plan_id" not in request.data:
                message = "plan_id is required!"
                return custom_response(False, status.HTTP_400_BAD_REQUEST, message)

            plan_check = Plan.objects.filter(pk=request.data['plan_id'], active=True)
            if not plan_check:
                message = "Invalid plan selected."
                return custom_response(False, status.HTTP_400_BAD_REQUEST, message)


            user = User.objects.get(pk=request.user.pk)
            if user.plan_id:
                if (user.plan_purchased_at + relativedelta(months=+user.plan_id.duration_in_months)) > datetime.now():
                    message = f"You are already associated with {user.plan_id.name} plan."
                    return custom_response(False, status.HTTP_400_BAD_REQUEST, message)

            if "card_id" in request.data:
                card_id = request.data["card_id"]
                stripe = MyStripe()
                customer_id = request.user.customer_id

                if not customer_id:
                    newcustomer = create_customer_id(request.user)
                    customer_id = newcustomer.id
                    print("<<<-----|| CUSTOMER CREATED ||----->>>")
                newcard = stripe.create_card(customer_id, request.data)
                card_id = newcard.id
                print("<<<-----|| CARD CREATED ||----->>>", plan_check[0])

                newcharge = stripe.create_charge(plan_check[0].plan_amount, card_id, customer_id)
                charge_object = create_charge_object(newcharge, request)

                chargeserializer = TransactionDetailSerializer(data=charge_object)
                if chargeserializer.is_valid():
                    chargeserializer.save()
                    print("<<<-----|| TransactionDetail CREATED ||----->>>")

                    transaction = TransactionDetail.objects.filter(pk=chargeserializer.data['id'])

                    user.plan_id = plan_check[0]
                    user.plan_purchased_at = datetime.now()
                    user.plan_purchase_detail = transaction[0]
                    message = "Plan purchased successfully!"
                    user.save()

                    if user.affiliated_with:
                        affiliation_record = CreatorAffiliation()
                        affiliation_record.user = user
                        affiliation_record.plan_id = plan_check[0]
                        affiliation_record.amount = plan_check[0].plan_amount
                        affiliation_record.save()

                    return custom_response(True, status.HTTP_201_CREATED, message)
            else:
                message = "Card_id is required"
                return custom_response(False, status.HTTP_400_BAD_REQUEST, message)

        except Exception as inst:
            print(inst)
            message = str(inst)
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)


class UserPlanAPIView(APIView):
    """
    User Profile view
    """
    serializer_class = UserPlanSerializer
    permission_classes = (IsAccountOwner, IsUser,)

    def get(self, request):
        user = get_object(User, request.user.pk)
        if not user.plan_id:
            message = "You dont have any active plan!"
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)
        if (user.plan_purchased_at + relativedelta(months=+user.plan_id.duration_in_months)) < datetime.now():
            message = "You dont have any active plan!"
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)
        serializer = self.serializer_class(user, context={"request": request})
        message = "plan Details fetched Successfully!"
        return custom_response(True, status.HTTP_200_OK, message, serializer.data)


class ForgotPasswordAPIView(APIView):
    """
    Send password reset link to email
    """
    def post(self, request, format=None):
        if "email" not in request.data.keys():
            message = "Email field is missing!"
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)
        try:
            user = User.objects.get(email=request.data['email'])
        except User.DoesNotExist:
            message = "User not found!"
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)

        user.password_reset_link = uuid.uuid4()
        user.save()
        subject= "[CreatorClasses] Request to change Password"
        text_content = f"Hello, \nYou recently requested to reset your password for your Creator Class account. Please click the below link to change your password. \n {settings.RESET_PASSWORD_LINK}{user.password_reset_link}"
        email_response = send_email(user, subject, text_content)              
        return custom_response(True, status.HTTP_200_OK, email_response)


class SetPasswordAPIView(APIView):
    """
    Set password view
    """
    def post(self, request, format=None):
        if "password" not in request.data:
            message = "Password field is missing!"
        if "token" not in request.data:
            message = "Token field is missing!"
        else:
            user = User.objects.filter(password_reset_link=request.data["token"]).first()
            if user:
                user.set_password(request.data["password"])
                user.password_reset_link = None
                user.save()
                message = "Password Changed Successfully!"
                return custom_response(True, status.HTTP_200_OK, message)
        message = "Invalid Token or link expired!"
        return custom_response(False, status.HTTP_400_BAD_REQUEST, message)