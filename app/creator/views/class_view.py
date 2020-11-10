from rest_framework.views import APIView
from ..serializers import AddClassSerializer, ClassListingSerializer, ClassDetailSerializer, AdminKeywordSerializer
from ..models import Creator, CreatorClass
from customadmin.models import AdminKeyword
from creator_class.helpers import custom_response, serialized_response, get_object
from rest_framework import status, renderers
from creator_class.permissions import IsAccountOwner, IsCreator


class AddClassAPIView(APIView):
    """
    Class view
    """
    serializer_class = AddClassSerializer
    permission_classes = (IsAccountOwner, IsCreator)

    def post(self, request, *args, **kwargs):
        request.data["creator"] = request.user.pk
        message = "Class created successfully!"
        serializer = self.serializer_class(data=request.data, context={"request": request})
        response_status, result, message = serialized_response(serializer, message)
        status_code = status.HTTP_201_CREATED if response_status else status.HTTP_400_BAD_REQUEST
        return custom_response(response_status, status_code, message, result)

    def put(self, request, pk, format=None):
        request.data["creator"] = request.user.pk
        class_exists = CreatorClass.objects.filter(pk=pk, active=True)
        if not class_exists:
            message = "Class not found!"
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)

        message = "Class updated successfully!"
        serializer = self.serializer_class(class_exists[0], data=request.data, partial=True, context={"request": request})
        response_status, result, message = serialized_response(serializer, message)
        status_code = status.HTTP_200_OK if response_status else status.HTTP_400_BAD_REQUEST
        if response_status:
            return custom_response(response_status, status_code, message)
        return custom_response(response_status, status_code, message, result)


    def delete(self, request, pk, format=None):
        class_exists = CreatorClass.objects.filter(pk=pk, active=True)
        if not class_exists:
            message = "Class not found!"
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)

        class_exists[0].active=False
        class_exists[0].save()
        message = "Class deleted successfully!"
        return custom_response(True, status.HTTP_200_OK, message)


class MyClassListingAPIView(APIView):
    """
    My class listing view
    """
    serializer_class = ClassListingSerializer
    permission_classes = (IsAccountOwner, IsCreator)

    def get(self, request):
        classes = CreatorClass.objects.filter(active=True, creator=request.user.pk)
        serializer = self.serializer_class(classes, many=True, context={"request": request})
        message = "Classes fetched Successfully!"
        return custom_response(True, status.HTTP_200_OK, message, serializer.data)


class ClassDetailAPIView(APIView):
    """
    Class detail view
    """
    serializer_class = ClassDetailSerializer
    permission_classes = ()

    def get(self, request, pk):
        creator_class = CreatorClass.objects.filter(active=True, pk=pk)
        if not creator_class:
            message = "Class not found"
            return custom_response(True, status.HTTP_400_BAD_REQUEST, message)
        serializer = self.serializer_class(creator_class[0],context={"request": request})
        message = "Class fetched Successfully!"
        return custom_response(True, status.HTTP_200_OK, message, serializer.data)


class KeywordsAPIView(APIView):
    """
    Keyword view
    """
    serializer_class = AdminKeywordSerializer
    permission_classes = ()

    def get(self, request):
        keywords = AdminKeyword.objects.filter(active=True)
        serializer = self.serializer_class(keywords, many=True, context={"request": request})
        message = "Keywords fetched Successfully!"
        return custom_response(True, status.HTTP_200_OK, message, serializer.data)