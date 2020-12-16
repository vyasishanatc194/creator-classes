from rest_framework import fields, serializers
from creator.models import Material
from creator.serializers import MaterialCategorySerializer


class UserMaterialListingSerializer(serializers.ModelSerializer):
    material_category = MaterialCategorySerializer()
    creator_name = serializers.SerializerMethodField()
    class Meta:
        model = Material
        fields = ['id', 'creator', 'creator_name', 'material_category', 'title', 'thumbnail_file', 'material_file']

    def get_creator_name(self, instance):
        return f"{instance.creator.first_name} {instance.creator.last_name}"