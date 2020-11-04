# from rest_framework.views import APIView
# from ..serializers import CreatorReviewSerializer, ClassReviewSerializer
# from ..models import FavouriteCreator, FavouriteClass
# from creator_class.helpers import custom_response, serialized_response
# from rest_framework import status, parsers, renderers
# from creator_class.permissions import IsAccountOwner, IsUser


# class FavouriteClassAPIView(APIView):
#     """
#     Favourite Class
#     """

#     serializer_class = FavouriteClassSerializer
#     permission_classes = (IsAccountOwner, IsUser)

#     def post(self, request, pk, format=None):
#         request_copy = request.data.copy()
#         request_copy["user"] = request.user.pk
#         request_copy["creator_class"] = pk

#         already_fav = FavouriteClass.objects.filter(user=request.user.pk, creator_class=pk)
#         if already_fav:
#             return custom_response(True, status.HTTP_201_CREATED, "Added Class to Favourites!")

#         serializer = self.serializer_class(data=request_copy)
#         message = "Added Class to Favourites!"
#         response_status, result, message = serialized_response(serializer, message)
#         status_code = (status.HTTP_200_OK if response_status else status.HTTP_400_BAD_REQUEST)
#         return custom_response(response_status, status_code, message, result)


#     def delete(self, request, pk, format=None):
#         FavouriteClass.objects.filter(pk=pk).delete()
#         message = "Class removed from favourites!"
#         return custom_response(True, status.HTTP_200_OK, message)


#     def get(self, request):
#         classes = FavouriteClass.objects.filter(user=request.user.pk)
#         serializer = self.serializer_class(classes, many=True, context={"request": request})
#         message = "Classes fetched Successfully!"
#         return custom_response(True, status.HTTP_200_OK, message, serializer.data)
