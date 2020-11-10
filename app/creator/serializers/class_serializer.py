from rest_framework import fields, serializers
from ..models import Creator, CreatorClass, ClassKeyword, ClassCovers, Material, ClassMaterial
from user.models import User, ClassReview, FavouriteClass
from django.db.models import Sum
from customadmin.models import AdminKeyword
from . import CreatorListingSerializer


class AddClassSerializer(serializers.ModelSerializer):
    """
    Add Class serializer
    """
    title = serializers.CharField(required=True)
    class_file = serializers.FileField(required=True)
    thumbnail_file = serializers.FileField(required=True)
    class_keywords = serializers.CharField()
    class_covers = serializers.CharField()
    class_materials = serializers.CharField(required=False)

    class Meta:
        model = CreatorClass
        fields = ['id', 'creator', 'title', 'thumbnail_file', 'class_file', 'class_keywords', 'class_covers', 'class_materials']

    def create(self, validated_data):
        class_keywords = validated_data.pop('class_keywords', None)
        class_covers = validated_data.pop('class_covers', None)
        class_materials = validated_data.pop('class_materials', None)
        creator_class =CreatorClass.objects.create(**validated_data)
        if class_keywords:
            class_keywords = class_keywords.split(',')
            for keyword in class_keywords:
                admin_keyword = AdminKeyword.objects.filter(pk=keyword)
                if admin_keyword:
                    ClassKeyword.objects.create(keyword=admin_keyword[0], creator_class=creator_class)

        if class_covers:
            class_covers = class_covers.split(',')
            for content in class_covers:
                ClassCovers.objects.create(covers=content, creator_class=creator_class)


        if class_materials:
            class_materials = class_materials.split(',')
            for class_material in class_materials:
                material = Material.objects.filter(pk=class_material)
                if material:
                    ClassMaterial.objects.create(creator_class=creator_class, class_material=material[0])

        creator_class.class_keywords = class_keywords
        creator_class.class_covers = class_covers
        creator_class.class_materials = class_materials
        return creator_class

    def update(self, instance, validated_data):
        class_keywords = validated_data.pop('class_keywords', None)
        class_covers = validated_data.pop('class_covers', None)
        class_materials = validated_data.pop('class_materials', None)
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
            instance.save()

        if class_keywords:
            class_keywords = class_keywords.split(',')
            ClassKeyword.objects.filter(creator_class=instance).delete()
            for keyword in class_keywords:
                admin_keyword = AdminKeyword.objects.filter(pk=keyword)
                if admin_keyword:
                    ClassKeyword.objects.create(keyword=admin_keyword[0], creator_class=instance)

        if class_covers:
            class_covers = class_covers.split(',')
            ClassCovers.objects.filter(creator_class=instance).delete()
            for covers in class_covers:
                ClassCovers.objects.create(covers=covers, creator_class=instance)

        if class_materials: 
            class_materials = class_materials.split(',')
            ClassMaterial.objects.filter(creator_class=instance).delete()
            for class_material in class_materials:
                material = Material.objects.filter(pk=class_material)
                if material:
                    ClassMaterial.objects.create(creator_class=instance, class_material=material[0])

        instance.class_keywords=class_keywords
        instance.class_covers=class_covers
        instance.class_materials=class_materials
        return instance


class ClassListingSerializer(serializers.ModelSerializer):
    """
    Class listing serializer
    """
    avg_rating = serializers.SerializerMethodField()
    total_rating = serializers.SerializerMethodField()
    creator_name = serializers.SerializerMethodField()
    is_favourite = serializers.SerializerMethodField()
    creator_profile_image = serializers.SerializerMethodField('get_profile_image_url')

    class Meta:
        model = CreatorClass
        fields = ['id', 'title', 'thumbnail_file', 'class_file', 'avg_rating', 'total_rating', 'creator_name', 'creator_profile_image', 'created_at', 'is_favourite']

    def get_avg_rating(self, instance):
        ratings = ClassReview.objects.filter(creator_class=instance)
        sum_ratings = ratings.aggregate(Sum('rating'))
        if sum_ratings['rating__sum'] and ratings.count():
            return sum_ratings['rating__sum']/ratings.count()
        return 0

    def get_total_rating(self, instance):
        ratings = ClassReview.objects.filter(creator_class=instance).count()
        return ratings

    def get_creator_name(self, instance):
        return f"{instance.creator.first_name} {instance.creator.last_name}"

    def get_is_favourite(self, instance):
        user = self.context['request'].user
        if not user.is_anonymous:
            is_favourite = FavouriteClass.objects.filter(creator_class=instance, user=user)
            return True if is_favourite else False
        return False

    def get_profile_image_url(self, creator_class):
        request = self.context.get('request')
        if creator_class.creator.profile_image:
            profile_image_url = creator_class.creator.profile_image.url
            return request.build_absolute_uri(profile_image_url)


class ClassMaterialListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['id', 'title', 'thumbnail_file', 'material_file']


class ClassCreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Creator
        fields = ['id', 'first_name', 'last_name', 'profile_image', 'key_skill', 'other_skills']


class ClassReviewListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    profile_image = serializers.SerializerMethodField('get_profile_image_url')
    class Meta:
        model = ClassReview
        fields = ['id', 'review', 'rating', 'username', 'first_name', 'last_name', 'profile_image']

    def get_profile_image_url(self, review_class):
        request = self.context.get('request')
        if review_class.user.profile_image:
            profile_image_url = review_class.user.profile_image.url
            return request.build_absolute_uri(profile_image_url)


class ClassDetailSerializer(serializers.ModelSerializer):
    """
    Class detail serializer
    """
    avg_rating = serializers.SerializerMethodField()
    total_rating = serializers.SerializerMethodField()
    class_keywords = serializers.SerializerMethodField()
    class_covers = serializers.SerializerMethodField()
    class_materials = serializers.SerializerMethodField()
    creator = CreatorListingSerializer()
    class_reviews = serializers.SerializerMethodField()
    is_favourite = serializers.SerializerMethodField()

    class Meta:
        model = CreatorClass
        fields = ['id', 'is_favourite', 'title', 'thumbnail_file', 'class_file', 'avg_rating', 'total_rating', 'creator', 'class_keywords', 'class_covers', 'class_materials', 'created_at', 'class_reviews']

    def get_avg_rating(self, instance):
        ratings = ClassReview.objects.filter(creator_class=instance)
        sum_ratings = ratings.aggregate(Sum('rating'))
        if sum_ratings['rating__sum'] and ratings.count():
            return sum_ratings['rating__sum']/ratings.count()
        return 0

    def get_total_rating(self, instance):
        ratings = ClassReview.objects.filter(creator_class=instance).count()
        return ratings

    def get_class_keywords(self, instance):
        class_keywords = ClassKeyword.objects.filter(creator_class=instance)
        return [class_keyword.keyword.keyword for class_keyword in class_keywords]

    def get_class_covers(self, instance):
        class_covers = ClassCovers.objects.filter(creator_class=instance)
        return [class_cover.covers for class_cover in class_covers]

    def get_class_materials(self, instance):
        class_materials = ClassMaterial.objects.filter(creator_class=instance).values('class_material__pk')
        materials = Material.objects.filter(pk__in=class_materials)
        serializer = ClassMaterialListSerializer(materials, many=True)
        return serializer.data

    def get_class_reviews(self, instance):
        reviews  = ClassReview.objects.filter(creator_class=instance)
        serializer = ClassReviewListSerializer(reviews, many=True, context={"request": self.context.get('request')})
        return serializer.data

    def get_is_favourite(self, instance):
        user = self.context['request'].user
        if not user.is_anonymous:
            is_favourite = FavouriteClass.objects.filter(creator_class=instance, user=user)
            return True if is_favourite else False
        return False


class AdminKeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminKeyword
        fields = ['id', 'keyword']


class PopularClassListingSerializer(serializers.ModelSerializer):
    """
    Class listing serializer
    """
    avg_rating = serializers.SerializerMethodField()
    total_rating = serializers.SerializerMethodField()
    creator_name = serializers.SerializerMethodField()
    is_favourite = serializers.SerializerMethodField()
    creator_profile_image = serializers.SerializerMethodField('get_profile_image_url')

    class Meta:
        model = CreatorClass
        fields = ['id', 'title', 'thumbnail_file', 'class_file', 'avg_rating', 'total_rating', 'creator_name', 'creator_profile_image', 'created_at', 'is_favourite']

    def get_avg_rating(self, instance):
        ratings = ClassReview.objects.filter(creator_class=instance)
        sum_ratings = ratings.aggregate(Sum('rating'))
        if sum_ratings['rating__sum'] and ratings.count():
            return sum_ratings['rating__sum']/ratings.count()
        return 0

    def get_total_rating(self, instance):
        ratings = ClassReview.objects.filter(creator_class=instance).count()
        return ratings

    def get_creator_name(self, instance):
        return f"{instance.creator.first_name} {instance.creator.last_name}"

    def get_is_favourite(self, instance):
        user = self.context['request'].user
        if not user.is_anonymous:
            is_favourite = FavouriteClass.objects.filter(creator_class=instance, user=user)
            return True if is_favourite else False
        return False

    def get_profile_image_url(self, creator_class):
        request = self.context.get('request')
        if creator_class.creator.profile_image:
            profile_image_url = creator_class.creator.profile_image.url
            return request.build_absolute_uri(profile_image_url)