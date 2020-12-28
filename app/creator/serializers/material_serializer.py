from rest_framework import fields, serializers
from ..models import MaterialCategory, Material


class MaterialCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialCategory
        fields = ['id', 'category_title', 'category_image']


class MaterialSerializer(serializers.ModelSerializer):
    material_category = serializers.CharField(required=True)
    title = serializers.CharField(required=True)
    thumbnail_file = serializers.FileField(required=True)
    material_file = serializers.FileField(required=True)
    class Meta:
        model = Material
        fields = ['id', 'creator', 'material_category', 'title', 'thumbnail_file', 'material_file']

    def create(self, validated_data):
        material_category = validated_data.pop('material_category', None)
        if material_category:
            validated_data['material_category'] = MaterialCategory.objects.get(pk=material_category)
        material = Material.objects.create(**validated_data)
        return material

    def update(self, instance, validated_data):
        material_category = validated_data.pop('material_category', None)
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        if material_category:
            instance.material_category = MaterialCategory.objects.get(pk=material_category)
        instance.save()
        return instance


class MaterialDetailSerializer(serializers.ModelSerializer):
    material_category = MaterialCategorySerializer()
    class Meta:
        model = Material
        fields = ['id', 'creator', 'material_category', 'title', 'thumbnail_file', 'material_file']

