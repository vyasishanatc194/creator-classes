from rest_framework.views import APIView
from ..serializers import MaterialCategorySerializer, MaterialSerializer
from ..models import MaterialCategory, Material
from creator_class.helpers import custom_response, serialized_response
from rest_framework import status, parsers
from creator_class.permissions import IsAccountOwner, IsCreator

NOT_FOUND_MESSAGE = "Material not found!"

class MaterialcategoryListingAPIView(APIView):
    """
    Material category listing
    """
    serializer_class = MaterialCategorySerializer
    def get(self, request):
        material_categories = MaterialCategory.objects.all()
        serializer = self.serializer_class(material_categories, many=True, context={"request": request})
        message = "Material categories fetched Successfully!"
        return custom_response(True, status.HTTP_200_OK, message, serializer.data)


class AddMaterialAPIView(APIView):
    """
    Material view
    """
    serializer_class = MaterialSerializer
    permission_classes = (IsAccountOwner, IsCreator)

    def post(self, request, *args, **kwargs):
        request.data["creator"] = request.user
        message = "Material created successfully!"
        serializer = self.serializer_class(data=request.data, context={"request": request})
        response_status, result, message = serialized_response(serializer, message)
        status_code = status.HTTP_201_CREATED if response_status else status.HTTP_400_BAD_REQUEST
        return custom_response(response_status, status_code, message, result)

    def put(self, request, pk, format=None):
        request.data["creator"] = request.user
        material_exists = Material.objects.filter(pk=pk, active=True)
        if not material_exists:
            return custom_response(False, status.HTTP_400_BAD_REQUEST, NOT_FOUND_MESSAGE)

        message = "Material updated successfully!"
        serializer = self.serializer_class(material_exists[0], data=request.data, partial=True, context={"request": request})
        response_status, result, message = serialized_response(serializer, message)
        status_code = status.HTTP_200_OK if response_status else status.HTTP_400_BAD_REQUEST
        if response_status:
            return custom_response(response_status, status_code, message)
        return custom_response(response_status, status_code, message, result)


    def delete(self, request, pk, format=None):
        material_exists = Material.objects.filter(pk=pk, active=True)
        if not material_exists:
            return custom_response(False, status.HTTP_400_BAD_REQUEST, NOT_FOUND_MESSAGE)

        material_exists[0].active=False
        material_exists[0].save()
        message = "Material deleted successfully!"
        return custom_response(True, status.HTTP_200_OK, message)

    
    def get(self, request, pk, format=None):
        material_exists = Material.objects.filter(pk=pk, active=True)
        if not material_exists:
            return custom_response(False, status.HTTP_400_BAD_REQUEST, NOT_FOUND_MESSAGE)
        serializer = self.serializer_class(material_exists[0], context={"request": request})
        message = "Material fetched Successfully!"
        return custom_response(True, status.HTTP_200_OK, message, serializer.data)


class MyMaterialAPIView(APIView):
    """
    My Material view
    """
    serializer_class = MaterialSerializer
    permission_classes = (IsAccountOwner, IsCreator)
    def get(self, request, format=None):
        materials = Material.objects.filter(active=True, creator=request.user.pk)
        if 'category' in request.GET:
            materials = materials.filter(material_category=request.GET['category'])

        serializer = self.serializer_class(materials, many=True, context={"request": request})
        message = "Materials fetched Successfully!"
        return custom_response(True, status.HTTP_200_OK, message, serializer.data)


class CreatorMaterialAPIView(APIView):
    """
    Creator Material view
    """
    serializer_class = MaterialSerializer

    def get(self, request, format=None):
        materials = Material.objects.filter(active=True)
        if 'creator' in request.GET:
            materials = materials.filter(creator=request.GET['creator'])

        serializer = self.serializer_class(materials, many=True, context={"request": request})
        message = "Materials fetched Successfully!"
        return custom_response(True, status.HTTP_200_OK, message, serializer.data)