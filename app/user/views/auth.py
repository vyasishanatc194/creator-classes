from rest_framework.views import APIView
from ..serializers import UserProfileSerializer, TestimonialListingSerializer, PlanListingSerializer
from ..models import User
from creator_class.helpers import custom_response, serialized_response
from rest_framework import status, parsers, renderers
from django.contrib.auth import authenticate, login, logout
from creator_class.permissions import IsAccountOwner

from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView

from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter
from rest_auth.social_serializers import TwitterLoginSerializer

from google.views import GoogleOAuth2Adapter
from rest_framework import generics
from customadmin.models import Testimonial, Plan



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
            serializer = self.serializer_class(data=request.data)
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


class TwitterLogin(SocialLoginView):
    serializer_class = TwitterLoginSerializer
    adapter_class = TwitterOAuthAdapter


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter


class TestimonialsListingAPIView(generics.ListCreateAPIView):
    queryset = Testimonial.objects.filter(active=True)
    serializer_class = TestimonialListingSerializer


class PlansListingAPIView(generics.ListCreateAPIView):
    queryset = Plan.objects.filter(active=True)
    serializer_class = PlanListingSerializer
