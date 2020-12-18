from rest_framework.views import APIView
from ..serializers import CreatorProfileSerializer, CreatorProfileDisplaySerializer, CreatorListingSerializer, CreatorRegisterSerializer, CreatorLoginSerializer
from ..models import Creator
from user.models import User
from creator_class.helpers import custom_response, serialized_response, get_object
from rest_framework import status, parsers, renderers
from django.contrib.auth import authenticate, login, logout
from creator_class.permissions import IsAccountOwner


class CreatorProfileAPI(APIView):
    """
    Creator Profile view
    """
    serializer_class = CreatorProfileSerializer
    permission_classes = (IsAccountOwner,)

    def put(self, request, *args, **kwargs):
        creator_profile = get_object(Creator, request.user.pk)
        if not creator_profile:
            message = "Creator not found!"
            return custom_response(True, status.HTTP_200_OK, message)
        message = "Profile updated successfully!"
        serializer = self.serializer_class(creator_profile, data=request.data, partial=True, context={"request": request})
        response_status, result, message = serialized_response(serializer, message)
        status_code = status.HTTP_201_CREATED if response_status else status.HTTP_400_BAD_REQUEST
        return custom_response(response_status, status_code, message, result)

    def get(self, request):
        creator_profile = get_object(Creator, request.user.pk)
        if not creator_profile:
            message = "Requested account details not found!"
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)
        serializer = CreatorProfileDisplaySerializer(creator_profile, context={"request": request})
        message = "Creator Details fetched Successfully!"
        return custom_response(True, status.HTTP_200_OK, message, serializer.data)


class CreatorDetailAPIView(APIView):
    def get(self, request,pk):
        creator_profile = get_object(Creator, pk)
        if not creator_profile:
            message = "Requested account details not found!"
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)
        serializer = CreatorProfileDisplaySerializer(creator_profile, context={"request": request})
        message = "Creator Details fetched Successfully!"
        return custom_response(True, status.HTTP_200_OK, message, serializer.data)



class CreatorListingAPIView(APIView):
    """
    Creator Profile view
    """
    serializer_class = CreatorListingSerializer
    def get(self, request):
        creators = Creator.objects.filter(is_active=True)

        key_skill = request.GET.get('key_skill', None)
        if key_skill:
            creators = creators.filter(key_skill=key_skill)

        serializer = self.serializer_class(creators, many=True, context={"request": request})
        message = "Creators fetched Successfully!"
        return custom_response(True, status.HTTP_200_OK, message, serializer.data)


class CreatorRegisterView(APIView):
    """
    Creator Register View
    """
    serializer_class = CreatorRegisterSerializer

    def post(self, request, *args, **kwargs):
        if 'email' in request.data:
            email_check = User.objects.filter(email=request.data['email']).distinct()
        if email_check.exists():
            return custom_response(False, status.HTTP_400_BAD_REQUEST, "Email already exists!")
        if 'username' in request.data:
            username_check = User.objects.filter(username=request.data['username']).distinct()
        if username_check.exists():
            return custom_response(False, status.HTTP_400_BAD_REQUEST, "Username already exists!")
        message = "Account registered successfully!"
        serializer = self.serializer_class(data=request.data, context={'request': request})
        response_status, result, message = serialized_response(serializer, message)
        status_code = status.HTTP_201_CREATED if response_status else status.HTTP_400_BAD_REQUEST
        # TODO Email
        return custom_response(response_status, status_code, message, result)



class CreatorLoginAPIView(APIView):
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
        email = request.data.get("email", None)
        password = request.data.get("password", None)

        if not email or not password:
            message = "Email and password is required"
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)
        
        creator_exist = Creator.objects.filter(email=email)
        if not creator_exist:
            message = "Email/password combination invalid"
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)
        
        if not creator_exist[0].check_password(password):
            message = "Email/password combination invalid"
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)        
        
        if not creator_exist[0].is_active:
            message = "Account is not activated by admin yet!"
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)
        login(request, creator_exist[0], backend='django.contrib.auth.backends.ModelBackend')
        serializer = CreatorLoginSerializer(creator_exist[0], context={'request':request})
        return custom_response(True, status.HTTP_200_OK, "Login Successful!", serializer.data)