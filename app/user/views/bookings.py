from rest_framework.views import APIView
from ..serializers import SessionBookingSerializer
from ..models import User, SessionBooking
from creator.models import TimeSlot
from creator_class.helpers import custom_response, serialized_response
from rest_framework import status
from creator_class.permissions import IsAccountOwner, IsUser


class OneToOneSessionBookingAPIView(APIView):
    """
    Booking for one to one session
    """
    serializer_class = SessionBookingSerializer
    permission_classes = (IsAccountOwner, IsUser)

    def post(self, request, format=None):
        request_copy = request.data.copy()
        request_copy["user"] = request.user.pk

        creator = request.data.pop('creator', None)
        time_slot = request.data.pop('time_slot', None)

        if not creator or not time_slot:
            message = "Please select time slot and creator!"
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)

        check_booked = TimeSlot.objects.filter(pk=time_slot, session__creator=creator)
        if not check_booked:
            message = "Time slot not found!"
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)

        if check_booked[0].is_booked:
            message = "Time slot not available!"
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)

        serializer = self.serializer_class(data=request_copy)
        message = "Session booked successfully!"
        response_status, result, message = serialized_response(serializer, message)
        if response_status:
            check_booked[0].is_booked = True
            check_booked[0].save()
            # TODO Send email
        
        status_code = (
            status.HTTP_200_OK if response_status else status.HTTP_400_BAD_REQUEST
        )

        return custom_response(response_status, status_code, message, result)

