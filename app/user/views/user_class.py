from rest_framework.views import APIView
from creator_class.helpers import custom_response, serialized_response
from rest_framework import status, parsers, renderers
from creator.serializers import ClassListingSerializer
from creator.models import CreatorClass, ClassKeyword
from ..models import ClassReview

CLASSES_FETCHED_MESSAGE = "Classes fetched Successfully!"


class ClassFilterAPIView(APIView):
    """
    Favourite Creator
    """
    serializer_class = ClassListingSerializer
    permission_classes = ()


    def get(self, request):
        search = request.GET.get('search', None)
        creator_classes = CreatorClass.objects.filter(active=True)
        creator_filter = request.GET.get('creator', None)
        filter_by = request.GET.get('filter_by', None)
        class_keyword = request.GET.get('class_keyword', None)
        if search:
            creator_classes = creator_classes.filter(title__icontains=search)
        if class_keyword:
            class_keyword = class_keyword.split(',')
            keyword_classes = []
            classes_keywords= ClassKeyword.objects.filter(keyword__in=class_keyword, creator_class__active=True)

            for classes in classes_keywords:
                if classes.creator_class not in keyword_classes:
                    keyword_classes.append(classes.creator_class)
            serializer = ClassListingSerializer(keyword_classes, many=True, context={"request": request})
            return custom_response(True, status.HTTP_200_OK, CLASSES_FETCHED_MESSAGE, serializer.data)

        if creator_filter:
            creator_classes = creator_classes.filter(creator=creator_filter)
        if filter_by=='new_first':
            creator_classes = creator_classes.order_by('-created_at')
        if filter_by=='old_first':
            creator_classes = creator_classes.order_by('created_at')
        if filter_by=='popularity':
            popular_classes = []
            class_reviews = ClassReview.objects.filter(creator_class__active=True).order_by('-rating')
            for classes in class_reviews:
                popular_classes.append(classes.creator_class)

            for classes in creator_classes:
                if classes not in popular_classes:
                    popular_classes.append(classes)

            serializer = ClassListingSerializer(popular_classes, many=True, context={"request": request})
            return custom_response(True, status.HTTP_200_OK, CLASSES_FETCHED_MESSAGE, serializer.data)
        serializer = ClassListingSerializer(creator_classes, many=True, context={"request": request})
        return custom_response(True, status.HTTP_200_OK, CLASSES_FETCHED_MESSAGE, serializer.data)


class ClassSearchAPIView(APIView):
    """
    Class Search API
    """
    serializer_class = ClassListingSerializer
    permission_classes = ()

    def get(self, request):
        search = request.GET.get('search', None)
        class_keyword = request.GET.get('class_keyword', None)
        exclude_class = request.GET.get('exclude_class', None)

        creator_classes = CreatorClass.objects.filter(active=True)
        if exclude_class:
            creator_classes = creator_classes.exclude(pk=exclude_class)

        if search:
            creator_classes = creator_classes.filter(title__icontains=search)

        if class_keyword:
            class_keyword = class_keyword.split(',')
            keyword_classes = []
            classes_keywords= ClassKeyword.objects.filter(keyword__in=class_keyword)

            for classes in classes_keywords:
                if classes.creator_class in creator_classes and classes.creator_class not in keyword_classes:
                    keyword_classes.append(classes.creator_class)
            serializer = ClassListingSerializer(keyword_classes, many=True, context={"request": request})
            return custom_response(True, status.HTTP_200_OK, CLASSES_FETCHED_MESSAGE, serializer.data) 


        serializer = ClassListingSerializer(creator_classes, many=True, context={"request": request})
        return custom_response(True, status.HTTP_200_OK, CLASSES_FETCHED_MESSAGE, serializer.data)