from rest_framework.views import APIView
from ..serializers import OneToOneSessionSerializer
from ..models import Creator, CreatorClass
from customadmin.models import AdminKeyword
from creator_class.helpers import custom_response, serialized_response, get_object
from rest_framework import status, renderers
from creator_class.permissions import IsAccountOwner, IsCreator


class OneToOneSessionAPIView(APIView):
    """
    Class view
    """
    serializer_class = OneToOneSessionSerializer
    permission_classes = (IsAccountOwner, IsCreator)

    def post(self, request, *args, **kwargs):
        request.data["creator"] = request.user.pk
        message = "One To One Session created successfully!"
        serializer = self.serializer_class(data=request.data, context={"request": request})
        response_status, result, message = serialized_response(serializer, message)
        status_code = status.HTTP_201_CREATED if response_status else status.HTTP_400_BAD_REQUEST
        return custom_response(response_status, status_code, message, result)

    # def put(self, request, pk, format=None):
    #     request.data["creator"] = request.user.pk
    #     class_exists = CreatorClass.objects.filter(pk=pk, active=True)
    #     if not class_exists:
    #         message = "Class not found!"
    #         return custom_response(False, status.HTTP_400_BAD_REQUEST, message)

    #     message = "Class updated successfully!"
    #     serializer = self.serializer_class(class_exists[0], data=request.data, partial=True, context={"request": request})
    #     response_status, result, message = serialized_response(serializer, message)
    #     status_code = status.HTTP_200_OK if response_status else status.HTTP_400_BAD_REQUEST
    #     if response_status:
    #         return custom_response(response_status, status_code, message)
    #     return custom_response(response_status, status_code, message, result)


    # def delete(self, request, pk, format=None):
    #     class_exists = CreatorClass.objects.filter(pk=pk, active=True)
    #     if not class_exists:
    #         message = "Class not found!"
    #         return custom_response(False, status.HTTP_400_BAD_REQUEST, message)

    #     class_exists[0].active=False
    #     class_exists[0].save()
    #     message = "Class deleted successfully!"
    #     return custom_response(True, status.HTTP_200_OK, message)