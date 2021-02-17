from rest_framework.views import APIView
from ..serializers import AddStreamSerializer, MyStreamSerializer, UpdateStreamSerializer
from creator_class.helpers import custom_response, serialized_response
from rest_framework import status
from creator_class.permissions import IsAccountOwner, IsCreator
from ..models import Stream
from datetime import datetime


class AddStreamAPIView(APIView):
    """
    Stream view
    """
    serializer_class = AddStreamSerializer
    permission_classes = (IsAccountOwner, IsCreator)

    def post(self, request, *args, **kwargs):
        request.data["creator"] = request.user.pk
        message = "Stream created successfully!"
        serializer = self.serializer_class(data=request.data, context={"request": request})
        response_status, result, message = serialized_response(serializer, message)
        status_code = status.HTTP_201_CREATED if response_status else status.HTTP_400_BAD_REQUEST
        return custom_response(response_status, status_code, message, result)

    def put(self, request, pk, format=None):
        stream_exists = Stream.objects.filter(pk=pk, active=True)
        if not stream_exists:
            message = "Stream not found!"
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)

        message = "Stream updated successfully!"
        serializer = UpdateStreamSerializer(stream_exists[0], data=request.data, partial=True, context={"request": request})
        response_status, result, message = serialized_response(serializer, message)
        status_code = status.HTTP_200_OK if response_status else status.HTTP_400_BAD_REQUEST
        return custom_response(response_status, status_code, message, result)

    def delete(self, request, pk, format=None):
        stream_exists = Stream.objects.filter(pk=pk, active=True)
        if not stream_exists:
            message = "Stream not found!"
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)

        stream_exists[0].active=False
        stream_exists[0].save()
        message = "Stream deleted successfully!"
        return custom_response(True, status.HTTP_200_OK, message)


class MyStreamListingAPIView(APIView):
    """
    My stream listing view
    """
    serializer_class = MyStreamSerializer
    permission_classes = (IsAccountOwner, IsCreator)

    def get(self, request):
        streams = Stream.objects.filter(active=True, creator=request.user.pk, stream_datetime__gte=datetime.now())
        serializer = self.serializer_class(streams, many=True, context={"request": request})
        message = "Streams fetched Successfully!"
        return custom_response(True, status.HTTP_200_OK, message, serializer.data)


class CreatorStreamListingAPIView(APIView):
    """
    My stream listing view
    """
    serializer_class = MyStreamSerializer

    def get(self, request):
        streams = Stream.objects.filter(active=True, stream_datetime__gte=datetime.today())
        if "creator" in request.GET:
            streams = streams.filter(creator=request.GET['creator'])

        serializer = self.serializer_class(streams, many=True, context={"request": request})
        message = "Streams fetched Successfully!"
        return custom_response(True, status.HTTP_200_OK, message, serializer.data)