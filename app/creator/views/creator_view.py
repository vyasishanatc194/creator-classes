from rest_framework.views import APIView
from ..serializers import CreatorProfileSerializer, CreatorProfileDisplaySerializer, CreatorListingSerializer
from ..models import Creator
from creator_class.helpers import custom_response, serialized_response, get_object
from rest_framework import status
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


class CreatorListingAPIView(APIView):
    """
    Creator Profile view
    """
    serializer_class = CreatorListingSerializer
    def get(self, request):
        creators = Creator.objects.filter(is_active=True)
        serializer = self.serializer_class(creators, many=True, context={"request": request})
        message = "Creators fetched Successfully!"
        return custom_response(True, status.HTTP_200_OK, message, serializer.data)
