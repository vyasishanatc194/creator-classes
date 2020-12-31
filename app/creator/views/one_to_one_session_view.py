from rest_framework.views import APIView
from ..serializers import OneToOneSessionSerializer, SessionListingSerializer, OneToOneSessionListingSerializer
from ..models import Creator, OneToOneSession, TimeSlot
from creator_class.helpers import custom_response, serialized_response
from rest_framework import status
from creator_class.permissions import IsAccountOwner, IsCreator
from datetime import datetime


class OneToOneSessionAPIView(APIView):
    """
    Class view
    """
    serializer_class = OneToOneSessionSerializer
    permission_classes = (IsCreator,)

    def post(self, request, *args, **kwargs):

        session_exists = OneToOneSession.objects.filter(creator=request.user.pk, active=True)
        if session_exists:
            message = "One to One session already exists!"
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)
        request_copy = request.data.copy()
        request_copy["creator"] = request.user.pk
        message = "One To One Session created successfully!"
        serializer = self.serializer_class(data=request_copy, context={"request": request})
        response_status, result, message = serialized_response(serializer, message)
        status_code = status.HTTP_201_CREATED if response_status else status.HTTP_400_BAD_REQUEST
        return custom_response(response_status, status_code, message)

    def put(self, request, format=None):
        request_copy = request.data.copy()
        request_copy["creator"] = request.user.pk
        session_exists = OneToOneSession.objects.filter(creator=request.user.pk, active=True)
        if not session_exists:
            message = "OneToOne Session not found!"
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)

        message = "Session updated successfully!"
        serializer = self.serializer_class(session_exists[0], data=request_copy, partial=True, context={"request": request})
        response_status, result, message = serialized_response(serializer, message)
        status_code = status.HTTP_200_OK if response_status else status.HTTP_400_BAD_REQUEST
        if response_status:
            return custom_response(response_status, status_code, message)
        return custom_response(response_status, status_code, message, result)

    def delete(self, request, pk, format=None):
        session_exists = TimeSlot.objects.filter(pk=pk, active=True)
        if not session_exists:
            message = "Session not found!"
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)

        if session_exists[0].is_booked:
            message = "You can't delete booked session!"
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)

        session_exists[0].delete()
        message = "Session deleted successfully!"
        return custom_response(True, status.HTTP_200_OK, message)

    def get(self, request):
        sessions = TimeSlot.objects.filter(active=True, slot_datetime__gte=datetime.now(), session__creator__pk=request.user.pk)
        serializer = SessionListingSerializer(sessions, many=True, context={"request": request})
        message = "Creator Sessions fetched Successfully!"
        return custom_response(True, status.HTTP_200_OK, message, serializer.data)


class CreatorSessionListingAPIView(APIView):
    """
    Creator session listing API
    """
    serializer_class = SessionListingSerializer

    def get(self, request, pk):
        sessions = TimeSlot.objects.filter(active=True, slot_datetime__gte=datetime.now(), session__creator__pk=pk, is_booked=False)
        serializer = self.serializer_class(sessions, many=True, context={"request": request})
        message = "Creator Sessions fetched Successfully!"
        result = {}
        result['time_slots'] = serializer.data
        creator_sessions = OneToOneSession.objects.filter(creator=pk)
        if creator_sessions:
            session_serializer = OneToOneSessionListingSerializer(creator_sessions[0], context={"request": request})
            result['session'] = session_serializer.data
        return custom_response(True, status.HTTP_200_OK, message, result)

