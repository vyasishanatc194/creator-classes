from rest_framework.views import APIView
from ..serializers import AddStreamSerializer
from creator_class.helpers import custom_response, serialized_response
from rest_framework import status
from creator_class.permissions import IsAccountOwner, IsCreator
from ..moels import Stream


class AddStreamAPIView(APIView):
    """
    Stream view
    """
    serializer_class = AddStreamSerializer
    permission_classes = (IsAccountOwner, IsCreator)

    def post(self, request, *args, **kwargs):
        request_copy = request.data
        request_copy["creator"] = request.user.pk
        message = "Stream created successfully!"
        serializer = self.serializer_class(data=request_copy, context={"request": request})
        response_status, result, message = serialized_response(serializer, message)
        status_code = status.HTTP_201_CREATED if response_status else status.HTTP_400_BAD_REQUEST
        return custom_response(response_status, status_code, message, result)

    def put(self, request, pk, format=None):
        request.data["creator"] = request.user.pk
        stream_exists = Stream.objects.filter(pk=pk, active=True)
        if not stream_exists:
            message = "Stream not found!"
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)

        message = "Stream updated successfully!"
        serializer = self.serializer_class(stream_exists[0], data=request.data, partial=True, context={"request": request})
        response_status, result, message = serialized_response(serializer, message)
        status_code = status.HTTP_200_OK if response_status else status.HTTP_400_BAD_REQUEST
        if response_status:
            return custom_response(response_status, status_code, message)
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