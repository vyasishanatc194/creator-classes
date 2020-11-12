from rest_framework.views import APIView
from ..serializers import OneToOneSessionSerializer
from ..models import Creator, CreatorClass, OneToOneSession
from creator_class.helpers import custom_response, serialized_response
from rest_framework import status
from creator_class.permissions import IsAccountOwner, IsCreator


class OneToOneSessionAPIView(APIView):
    """
    Class view
    """
    serializer_class = OneToOneSessionSerializer
    permission_classes = (IsAccountOwner, IsCreator)

    def post(self, request, *args, **kwargs):
        request_copy = request.data.copy()
        request_copy["creator"] = request.user.pk
        message = "One To One Session created successfully!"
        print("request_copy", request_copy)
        serializer = self.serializer_class(data=request_copy, context={"request": request})
        response_status, result, message = serialized_response(serializer, message)
        status_code = status.HTTP_201_CREATED if response_status else status.HTTP_400_BAD_REQUEST
        return custom_response(response_status, status_code, message, result)

    def put(self, request, pk, format=None):
        request.data["creator"] = request.user.pk
        session_exists = OneToOneSession.objects.filter(pk=pk, active=True)
        if not session_exists:
            message = "OneToOne Session not found!"
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)

        message = "Session updated successfully!"
        serializer = self.serializer_class(class_exists[0], data=request.data, partial=True, context={"request": request})
        response_status, result, message = serialized_response(serializer, message)
        status_code = status.HTTP_200_OK if response_status else status.HTTP_400_BAD_REQUEST
        if response_status:
            return custom_response(response_status, status_code, message)
        return custom_response(response_status, status_code, message, result)


    def delete(self, request, pk, format=None):
        session_exists = OneToOneSession.objects.filter(pk=pk, active=True)
        if not session_exists:
            message = "Session not found!"
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)

        session_exists[0].active=False
        session_exists[0].save()
        message = "Session deleted successfully!"
        return custom_response(True, status.HTTP_200_OK, message)