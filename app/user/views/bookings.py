from rest_framework.views import APIView
from ..serializers import SessionBookingSerializer, TransactionDetailSerializer
from ..models import User, SessionBooking, TransactionDetail, BookedSessionKeywords
from creator.models import TimeSlot
from creator_class.helpers import custom_response, serialized_response
from rest_framework import status
from creator_class.permissions import IsAccountOwner, IsUser
from creator_class.utils import MyStripe, create_card_object, create_customer_id, create_charge_object
from customadmin.models import AdminKeyword


class OneToOneSessionBookingAPIView(APIView):
    """
    API View to purchase product
    """
    permission_classes = (IsAccountOwner, IsUser)

    def post(self, request, format=None):
        """POST method to create the data"""
        try:
            if "creator" not in request.data:
                message = "creator is required!"
                return custom_response(False, status.HTTP_400_BAD_REQUEST, message)

            if "time_slot" not in request.data :
                message = "time_slot is required!"
                return custom_response(False, status.HTTP_400_BAD_REQUEST, message)

            check_booking = TimeSlot.objects.filter(pk=request.data['time_slot'], session__creator__pk=request.data['creator'])
            if check_booking and check_booking[0].is_booked:
                message = "This time slot is already booked. Please select another."
                return custom_response(False, status.HTTP_400_BAD_REQUEST, message)

            if "card_id" in request.data:
                card_id = request.data["card_id"]
                stripe = MyStripe()
                customer_id = request.user.customer_id

                if not customer_id:
                    newcustomer = create_customer_id(request.user)
                    customer_id = newcustomer.id
                    print("<<<-----|| CUSTOMER CREATED ||----->>>")
                newcard = stripe.create_card(customer_id, request.data)
                card_id = newcard.id
                print("<<<-----|| CARD CREATED ||----->>>", check_booking[0])

                newcharge = stripe.create_charge(check_booking[0].session.amount, card_id, customer_id)
                charge_object = create_charge_object(newcharge, request)

                chargeserializer = TransactionDetailSerializer(data=charge_object)
                if chargeserializer.is_valid():
                    chargeserializer.save()
                    print("<<<-----|| TransactionDetail CREATED ||----->>>")

                    transaction = TransactionDetail.objects.filter(pk=chargeserializer.data['id'])

                    session_booking = SessionBooking()
                    session_booking.user = request.user
                    session_booking.creator = check_booking[0].session.creator
                    session_booking.time_slot = check_booking[0]
                    session_booking.card_id = request.data['card_id']
                    session_booking.transaction_detail = transaction[0]
                    if "description" in request.data:
                        session_booking.description=request.data['description']
                    session_booking.save()
                    message = "Session booked successfully!"

                    check_booking[0].is_booked=True
                    check_booking[0].save()
                    if 'keywords' in request.data:
                        keywords = request.data['keywords'].split(',')
                        for keyword in keywords:
                            keyword_exists = AdminKeyword.objects.filter(pk=keyword)
                            if keyword_exists:
                                session_keywords =BookedSessionKeywords()
                                session_keywords.session = session_booking
                                session_keywords.keyword =keyword_exists[0]
                                session_keywords.save()


                    return custom_response(True, status.HTTP_201_CREATED, message)
            else:
                message = "Card_id is required"
                return custom_response(False, status.HTTP_400_BAD_REQUEST, message)

        except Exception as inst:
            print(inst)
            message = str(inst)
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)
