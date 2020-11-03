from rest_framework.views import APIView
from ..serializers import CreatorReviewSerializer
from ..models import User, CreatorReview
from creator_class.helpers import custom_response, serialized_response
from rest_framework import status, parsers, renderers
from creator_class.permissions import IsAccountOwner, IsUser


class CreatorReviewAPIView(APIView):
    """
    Add ReviewAndRating for store
    """

    serializer_class = CreatorReviewSerializer
    permission_classes = (IsAccountOwner, IsUser)

    def post(self, request, format=None):
        request_copy = request.data.copy()
        request_copy["user"] = request.user.pk
        
        if "rating" in request_copy:
            if int(request_copy['rating']) > 5 or int(request_copy['rating']) < 1:
                message = "Enter valid rating!"
                return custom_response(False, status.HTTP_400_BAD_REQUEST, message)

        already_reviewed = CreatorReview.objects.filter(user=request.user.pk, creator=request.data['creator'])
        if already_reviewed:
            already_reviewed[0].delete()

        serializer = self.serializer_class(data=request_copy)
        message = "Review added successfully!"
        response_status, result, message = serialized_response(serializer, message)
        
        status_code = (
            status.HTTP_200_OK if response_status else status.HTTP_400_BAD_REQUEST
        )

        return custom_response(response_status, status_code, message, result)


    def delete(self, request, pk, format=None):
        already_reviewed = CreatorReview.objects.filter(pk=pk)
        if not already_reviewed:
            message = "Review not found!"
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)
        
        already_reviewed[0].delete()
        message = "Review deleted successfully!"
        return custom_response(True, status.HTTP_200_OK, message)


    def put(self, request, pk, format=None):
        request_copy = request.data.copy()
        request_copy["user"] = request.user.pk
        already_reviewed = CreatorReview.objects.filter(pk=pk)

        if not already_reviewed:
            message = "Review not found!"
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)

        message = "Review updated successfully!"
        serializer = self.serializer_class(already_reviewed[0], data=request_copy, partial=True, context={"request": request})
        response_status, result, message = serialized_response(serializer, message)
        status_code = status.HTTP_201_CREATED if response_status else status.HTTP_400_BAD_REQUEST
        return custom_response(response_status, status_code, message, result)