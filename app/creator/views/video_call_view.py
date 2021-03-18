from rest_framework.views import APIView
from creator_class.helpers import custom_response, serialized_response
from rest_framework import status
from creator_class.permissions import IsAccountOwner, IsCreator
from ..models import Stream, TimeSlot
from datetime import datetime
from creator_class.settings import(
    AgoraAppID,
    AgoraAppCertificate,
)
import time
from .RtcTokenBuilder import RtcTokenBuilder
expireTimeInSeconds = 3600
currentTimestamp = int(time.time())
privilegeExpiredTs = currentTimestamp + expireTimeInSeconds
import random


class GenerateAgoraTokenAPIView(APIView):
    """
    GenerateAgoraTokenAPIView
    """
    permission_classes = (IsAccountOwner, IsCreator)

    def get(self, request):
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

            if stream.agora_token:
                message = "Call has already started!"    
                return custom_response(False, status.HTTP_400_BAD_REQUEST, message)

            channel_name = stream.title
            uid = random.getrandbits(32)

            token = RtcTokenBuilder.buildTokenWithUid(
                AgoraAppID, AgoraAppCertificate,
                channel_name,
                uid,      #uid
                1,      #Role_Publisher
                privilegeExpiredTs
            )

            stream.channel_name = channel_name
            stream.agora_uid = uid
            stream.agora_token = token
            stream.token_created_at = datetime.now()
            stream.save()
            data = {
                "channel_name" : channel_name,
                "uid" : uid,
                "appID" : AgoraAppID,
                "token" : token,
                "AgoraAppCertificate" : AgoraAppCertificate
            }
        
        if call_type == valid_call_type[1]:
            sessions = TimeSlot.objects.filter(pk=call_id, session__creator=request.user.pk)
            if not sessions:
                message = "Invalid Session ID!"    
                return custom_response(False, status.HTTP_400_BAD_REQUEST, message)
            session = sessions.first()

            if session.agora_token:
                message = "Call has already started!"    
                return custom_response(False, status.HTTP_400_BAD_REQUEST, message)

            channel_name = session.session.creator.first_name + " " + session.session.creator.last_name
            uid = random.getrandbits(32)

            token = RtcTokenBuilder.buildTokenWithUid(
                AgoraAppID, AgoraAppCertificate,
                channel_name,
                uid,      #uid
                1,      #Role_Publisher
                privilegeExpiredTs
            )

            session.channel_name = channel_name
            session.agora_uid = uid
            session.agora_token = token
            session.token_created_at = datetime.now()
            session.save()
            data = {
                "channel_name" : channel_name,
                "uid" : uid,
                "appID" : AgoraAppID,
                "token" : token,
                "AgoraAppCertificate" : AgoraAppCertificate
            }
        
        message = "Channel created Successfully!"
        return custom_response(True, status.HTTP_200_OK, message, data)


class SessionScreenShareAPIView(APIView):
    """
    GenerateAgoraTokenAPIView
    """
    permission_classes = (IsAccountOwner,)

    def post(self, request, pk):
        screen_share = request.GET.get('screen_share', False)
        sessions = TimeSlot.objects.filter(pk=pk)
        if not sessions:
            message = "Session not found!"    
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)
        session = sessions.first()
        session.screen_share = screen_share
        session.save()        
        message = "Screen share status updated Successfully!"
        return custom_response(True, status.HTTP_200_OK, message)


    def get(self, request, pk):
        sessions = TimeSlot.objects.filter(pk=pk)
        if not sessions:
            message = "Session not found!"    
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)
        session = sessions.first()
        data = {
            "screen_share": session.screen_share
        } 
        message = "Screen share status updated Successfully!"
        return custom_response(True, status.HTTP_200_OK, message, data)


class EndCallAPIView(APIView):
    """
    EndCallAPIView
    """
    permission_classes = (IsAccountOwner, IsCreator)

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
            stream.completed = True
            stream.stream_completed_at = datetime.now()
            stream.save()

        if call_type == valid_call_type[1]:
            sessions = TimeSlot.objects.filter(pk=call_id, session__creator=request.user.pk)
            if not sessions:
                message = "Invalid Session ID!"    
                return custom_response(False, status.HTTP_400_BAD_REQUEST, message)
            session = sessions.first()
            session.completed = True
            session.session_completed_at = datetime.now()
            session.save()          
  
        message = "Call ended successfully!"
        return custom_response(True, status.HTTP_200_OK, message)


    def get(self, request):
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
            completed = stream.completed

        if call_type == valid_call_type[1]:
            sessions = TimeSlot.objects.filter(pk=call_id, session__creator=request.user.pk)
            if not sessions:
                message = "Invalid Session ID!"    
                return custom_response(False, status.HTTP_400_BAD_REQUEST, message)
            session = sessions.first()
            completed = session.completed        
  
        message = "Call status fetched successfully!"
        return custom_response(True, status.HTTP_200_OK, message, {'completed': completed})