from rest_framework.views import APIView
from creator_class.helpers import custom_response, serialized_response
from rest_framework import status, parsers, renderers
from ..serializers import UserMaterialListingSerializer
from creator.serializers import MaterialCategorySerializer
from creator.models import Material, MaterialCategory


class MaterialListingAPIView(APIView):
    """
    Material Listing view
    """
    serializer_class = UserMaterialListingSerializer
    def get(self, request, format=None):
        materials = Material.objects.filter(active=True)
        if 'category' in request.GET:
            materials = materials.filter(material_category=request.GET['category'])
        serializer = self.serializer_class(materials, many=True, context={"request": request})
        message = "Materials fetched Successfully!"
        result = serializer.data
        
        if 'category' in request.GET:
            category = MaterialCategory.objects.filter(pk=request.GET['category'])
            if category:
                category_serializer = MaterialCategorySerializer(category[0], context={"request": request})
                result.append({'category_detail':category_serializer.data})

        return custom_response(True, status.HTTP_200_OK, message, result)