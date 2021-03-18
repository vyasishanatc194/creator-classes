from rest_framework.views import APIView
from creator_class.helpers import custom_response, serialized_response
from rest_framework import status
from creator_class.permissions import IsAccountOwner, IsUser
from creator.models import Stream, TimeSlot
from ..models import SessionBooking, StreamBooking
from datetime import datetime
from creator_class.settings import(
    AgoraAppID,
    AgoraAppCertificate,
)


class JoinCallAPIView(APIView):
    """
    EndCallAPIView
    """
    permission_classes = (IsAccountOwner, IsUser)

    def post(self, request):
        call_type = request.GET.get('call_type', None)
        call_id = request.GET.get('call_id', None)
        if not call_type or not call_id:
            message = "call_type and call_id are required!"    
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)

        valid_call_type = ['stream', 'session']
        if call_type not in valid_call_type:
            message = "Invalid call_type. Choose from " + str(valid_call_type)    
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)

        if call_type == valid_call_type[0]:
            streams = Stream.objects.filter(pk=call_id, creator=request.user.pk)
            if not streams:
                message = "Invalid Stream ID!"    
                return custom_response(False, status.HTTP_400_BAD_REQUEST, message)
            stream = streams.first()

            user_booking = StreamBooking.objects.filter(user=request.user.pk, stream=stream.pk)
            if not user_booking:
                message = "You are not allowed to join the Live stream!"    
                return custom_response(False, status.HTTP_400_BAD_REQUEST, message)
            booking = user_booking.first()
            booking.user_joined = True
            booking.save()

            data = {
                "channel_name" : stream.channel_name,
                "uid" : stream.uid,
                "appID" : AgoraAppID,
                "token" : stream.agora_token,
                "AgoraAppCertificate" : AgoraAppCertificate
            }

        if call_type == valid_call_type[1]:
            sessions = TimeSlot.objects.filter(pk=call_id, session__creator=request.user.pk)
            if not sessions:
                message = "Invalid Session ID!"    
                return custom_response(False, status.HTTP_400_BAD_REQUEST, message)
            session = sessions.first()

            user_booking = SessionBooking.objects.filter(user=request.user.pk, time_slot=session)
            if not user_booking:
                message = "You are not allowed to join the session!"
                return custom_response(False, status.HTTP_400_BAD_REQUEST, message)
            booking = user_booking.first()
            booking.user_joined = True
            booking.save()

            session.completed = True
            session.session_completed_at = datetime.now()
            session.save()

            data = {
                "channel_name" : session.channel_name,
                "uid" : session.uid,
                "appID" : AgoraAppID,
                "token" : session.agora_token,
                "AgoraAppCertificate" : AgoraAppCertificate
            } 
  
        message = "Call ended successfully!"
        return custom_response(True, status.HTTP_200_OK, message, data)

