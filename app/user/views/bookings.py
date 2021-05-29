from rest_framework.views import APIView
from ..serializers import SessionBookingSerializer, TransactionDetailSerializer, StreamSeatHolderSerializer, SessionSeatHolderSerializer, UserBookedStreamListingSerializer, UserBookedSessionListingSerializer
from ..models import User, SessionBooking, TransactionDetail, BookedSessionKeywords, StreamBooking, Notification
from creator.models import TimeSlot, Stream
from creator_class.helpers import custom_response, serialized_response, send_templated_email
from rest_framework import status
from creator_class.permissions import IsAccountOwner, IsUser, IsCreator, get_pagination_response
from creator_class.utils import MyStripe, create_card_object, create_customer_id, create_charge_object
from customadmin.models import AdminKeyword
from datetime import datetime

from creator_class import settings

class OneToOneSessionBookingAPIView(APIView):
    """
    API View to book One to One Session
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

                newcharge = stripe.create_charge((check_booking[0].session.amount)*100, card_id, customer_id)
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
                    notification_creator = Notification()
                    notification_creator.notification_type= "BOOKING"
                    notification_creator.user = check_booking[0].session.creator
                    notification_creator.description = f"{request.user.username} booked one to one session with you on {check_booking[0].slot_datetime}"
                    notification_creator.title = "Booking"
                    notification_creator.profile_image = request.user.profile_image
                    notification_creator.save()

                    notification_user = Notification()
                    notification_user.notification_type= "BOOKING"
                    notification_user.user = request.user
                    notification_user.title = "Booking"
                    notification_user.profile_image = check_booking[0].session.creator.profile_image
                    notification_user.description = f"Your one to one session with {check_booking[0].session.creator.first_name} {check_booking[0].session.creator.last_name} at {check_booking[0].slot_datetime} is booked successfully"
                    notification_user.save()

                    name = request.user.username if request.user.username else f"{request.user.first_name} {request.user.last_name}"
                    if request.user.email:
                        email_data = {
                            'name': name,
                            'date': check_booking[0].slot_datetime.date().strftime('%m/%d/%Y'),
                            'time': check_booking[0].slot_datetime.time().strftime("%H:%M"),
                            'creator_name': f"{check_booking[0].session.creator.first_name} {check_booking[0].session.creator.last_name}"
                        }
                        send_templated_email(request.user.email, settings.USER_SESSION_BOOKING, email_data)

                    # Creator Email
                    name = request.user.username if request.user.username else f"{request.user.first_name} {request.user.last_name}"
                    email_data = {
                        'name': f"{check_booking[0].session.creator.first_name} {check_booking[0].session.creator.last_name}",
                        'user_name': name,
                        'date': check_booking[0].slot_datetime.date().strftime('%m/%d/%Y'),
                        'time': check_booking[0].slot_datetime.time().strftime("%H:%M"),
                        'comments': session_booking.description,
                        'cost': check_booking[0].session.amount,
                    }
                    send_templated_email(check_booking[0].session.creator.email, settings.CREATOR_SESSION_BOOKING,
                                         email_data)

                    return custom_response(True, status.HTTP_201_CREATED, message)
            else:
                if check_booking:
                    if check_booking[0].session.amount == 0:
                        session_booking = SessionBooking()
                        session_booking.user = request.user
                        session_booking.creator = check_booking[0].session.creator
                        session_booking.time_slot = check_booking[0]
                        if "description" in request.data:
                            session_booking.description = request.data['description']
                        session_booking.save()
                        message = "Session booked successfully!"

                        check_booking[0].is_booked = True
                        check_booking[0].save()
                        if 'keywords' in request.data:
                            keywords = request.data['keywords'].split(',')
                            for keyword in keywords:
                                keyword_exists = AdminKeyword.objects.filter(pk=keyword)
                                if keyword_exists:
                                    session_keywords = BookedSessionKeywords()
                                    session_keywords.session = session_booking
                                    session_keywords.keyword = keyword_exists[0]
                                    session_keywords.save()
                        notification_creator = Notification()
                        notification_creator.notification_type = "BOOKING"
                        notification_creator.user = check_booking[0].session.creator
                        notification_creator.description = f"{request.user.username} booked one to one session with you on {check_booking[0].slot_datetime}"
                        notification_creator.title = "Booking"
                        notification_creator.profile_image = request.user.profile_image
                        notification_creator.save()

                        notification_user = Notification()
                        notification_user.notification_type = "BOOKING"
                        notification_user.user = request.user
                        notification_user.title = "Booking"
                        notification_user.profile_image = check_booking[0].session.creator.profile_image
                        notification_user.description = f"Your one to one session with {check_booking[0].session.creator.first_name} {check_booking[0].session.creator.last_name} at {check_booking[0].slot_datetime} is booked successfully"
                        notification_user.save()

                        name = request.user.username if request.user.username else f"{request.user.first_name} {request.user.last_name}"
                        if request.user.email:
                            email_data = {
                                'name': name,
                                'date': check_booking[0].slot_datetime.date().strftime('%m/%d/%Y'),
                                'time': check_booking[0].slot_datetime.time().strftime("%H:%M"),
                                'creator_name': f"{check_booking[0].session.creator.first_name} {check_booking[0].session.creator.last_name}"
                            }
                            send_templated_email(request.user.email, settings.USER_SESSION_BOOKING, email_data)

                        # Creator Email
                        name = request.user.username if request.user.username else f"{request.user.first_name} {request.user.last_name}"
                        email_data = {
                            'name': f"{check_booking[0].session.creator.first_name} {check_booking[0].session.creator.last_name}",
                            'user_name': name,
                            'date': check_booking[0].slot_datetime.date().strftime('%m/%d/%Y'),
                            'time': check_booking[0].slot_datetime.time().strftime("%H:%M"),
                            'comments': session_booking.description,
                            'cost': check_booking[0].session.amount,
                        }
                        send_templated_email(check_booking[0].session.creator.email, settings.CREATOR_SESSION_BOOKING,
                                             email_data)

                        return custom_response(True, status.HTTP_201_CREATED, message)

                message = "Card_id is required"
                return custom_response(False, status.HTTP_400_BAD_REQUEST, message)

        except Exception as inst:
            print(inst)
            message = str(inst)
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)


class StreamBookingAPIView(APIView):
    """
    API View to book stream
    """
    permission_classes = (IsAccountOwner, IsUser)

    def post(self, request, format=None):
        """POST method to create the data"""
        try:
            if "stream" not in request.data:
                message = "Stream is required!"
                return custom_response(False, status.HTTP_400_BAD_REQUEST, message)

            streams = Stream.objects.filter(pk=request.data['stream'], active=True, stream_datetime__gt=datetime.now())
            if not streams:
                message = "Stream not found!"
                return custom_response(False, status.HTTP_400_BAD_REQUEST, message)

            check_seats = StreamBooking.objects.filter(stream=request.data['stream'])
            if check_seats.count() >= streams[0].total_seats:
                message = "All seats are booked for this stream."
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
                print("<<<-----|| CARD CREATED ||----->>>")

                newcharge = stripe.create_charge(streams[0].stream_amount * 100, card_id, customer_id)
                charge_object = create_charge_object(newcharge, request)

                chargeserializer = TransactionDetailSerializer(data=charge_object)
                if chargeserializer.is_valid():
                    chargeserializer.save()
                    print("<<<-----|| TransactionDetail CREATED ||----->>>")

                    transaction = TransactionDetail.objects.filter(pk=chargeserializer.data['id'])

                    stream_booking = StreamBooking()
                    stream_booking.stream = streams[0]
                    stream_booking.user = request.user
                    stream_booking.card_id = request.data['card_id']
                    stream_booking.transaction_detail = transaction[0]
                    message = "Stream booked successfully!"
                    stream_booking.save()

                    notification_creator = Notification()
                    notification_creator.notification_type= "BOOKING"
                    notification_creator.user = check_seats[0].stream.creator
                    notification_creator.description = f"{request.user.username} booked a seat for {streams[0].title}"
                    notification_creator.title = "Booking"
                    notification_creator.profile_image = request.user.profile_image
                    notification_creator.save()

                    notification_user = Notification()
                    notification_user.notification_type= "BOOKING"
                    notification_user.user = request.user
                    notification_user.description = f"Your seat is booked for {streams[0].title} stream."
                    notification_user.title = "Booking"
                    notification_user.profile_image = streams[0].creator.profile_image
                    notification_user.save()

                    # User Email
                    name = request.user.username if request.user.username else f"{request.user.first_name} {request.user.last_name}"
                    if request.user.email:
                        email_data = {
                            'name': name,
                            'date': streams[0].stream_datetime.date().strftime('%m/%d/%Y'),
                            'time': streams[0].stream_datetime.time().strftime("%H:%M"),
                            'stream_name': streams[0].title,
                            'creator_name': f"{streams[0].creator.first_name} {streams[0].creator.last_name}"
                        }
                        send_templated_email(request.user.email, settings.USER_LIVE_STREAM_BOOKING_TEMPLATE, email_data)

                    # Creator Email
                    name = request.user.username if request.user.username else f"{request.user.first_name} {request.user.last_name}"
                    email_data = {
                        'name': f"{streams[0].creator.first_name} {streams[0].creator.last_name}",
                        'user_name': name,
                        'date': streams[0].stream_datetime.date().strftime('%m/%d/%Y'),
                        'time': streams[0].stream_datetime.time().strftime("%H:%M"),
                        'stream_name': streams[0].title,
                        'cost': streams[0].stream_amount,
                        'seats_left': streams[0].total_seats - (check_seats.count())
                    }
                    send_templated_email(streams[0].creator.email, settings.CREATOR_LIVE_STREAM_BOOKING_TEMPLATE,
                                         email_data)

                    return custom_response(True, status.HTTP_201_CREATED, message)
            else:
                message = "Card_id is required"
                return custom_response(False, status.HTTP_400_BAD_REQUEST, message)

        except Exception as inst:
            print(inst)
            message = str(inst)
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)


class StreamSeatHolderAPIView(APIView):
    """
    List of seat holders
    """
    serializer_class = StreamSeatHolderSerializer
    permission_classes = (IsCreator,)

    def get(self, request, pk):
        seat_holders = StreamBooking.objects.filter(active=True, stream=pk)
        serializer = StreamSeatHolderSerializer(seat_holders, many=True, context={"request": request})
        message = "Seat holders fetched successfully!"
        return custom_response(True, status.HTTP_200_OK, message, serializer.data)


class BookedSessionSeatholdersAPIView(APIView):
    """
    List of seat holders
    """
    serializer_class = SessionSeatHolderSerializer
    permission_classes = (IsCreator,)

    def get(self, request):
        seat_holders = SessionBooking.objects.filter(active=True, creator=request.user.pk, time_slot__slot_datetime__gte=datetime.now())
        serializer = SessionSeatHolderSerializer(seat_holders, many=True, context={"request": request})
        message = "Seat holders fetched successfully!"
        return custom_response(True, status.HTTP_200_OK, message, serializer.data)



class PayPalStreamBookingAPIView(APIView):
    """
    API View to book stream with PayPal
    """
    permission_classes = (IsAccountOwner, IsUser)

    def post(self, request, format=None):
        """POST method to create the data"""
        try:
            if "stream" not in request.data:
                message = "Stream is required!"
                return custom_response(False, status.HTTP_400_BAD_REQUEST, message)

            streams = Stream.objects.filter(pk=request.data['stream'], active=True, stream_datetime__gt=datetime.now())
            if not streams:
                message = "Stream not found!"
                return custom_response(False, status.HTTP_400_BAD_REQUEST, message)

            request_copy = request.data.copy()
            request_copy["user"] = request.user.pk
            check_seats = StreamBooking.objects.filter(stream=request.data['stream'])
            if check_seats.count() >= streams[0].total_seats:
                message = "All seats are booked for this stream."
                return custom_response(False, status.HTTP_400_BAD_REQUEST, message)
            chargeserializer = TransactionDetailSerializer(data=request_copy)
            if chargeserializer.is_valid():
                chargeserializer.save()
                print("<<<-----|| TransactionDetail CREATED ||----->>>")

                transaction = TransactionDetail.objects.filter(pk=chargeserializer.data['id'])

                stream_booking = StreamBooking()
                stream_booking.stream = streams[0]
                stream_booking.user = request.user
                stream_booking.card_id = request.data['brand']
                stream_booking.transaction_detail = transaction[0]
                message = "Stream booked successfully!"
                stream_booking.save()

                notification_creator = Notification()
                notification_creator.notification_type= "BOOKING"
                notification_creator.user = streams[0].creator
                notification_creator.description = f"{request.user.username} booked a seat for {streams[0].title}"
                notification_creator.title = "Booking"
                notification_creator.profile_image = request.user.profile_image
                notification_creator.save()

                notification_user = Notification()
                notification_user.notification_type= "BOOKING"
                notification_user.user = request.user
                notification_user.description = f"Your seat is booked for {streams[0].title} stream."
                notification_user.title = "Booking"
                notification_user.profile_image = streams[0].creator.profile_image
                notification_user.save()

                # User Email
                name = request.user.username if request.user.username else f"{request.user.first_name} {request.user.last_name}"
                if request.user.email:
                    email_data = {
                        'name': name,
                        'date': streams[0].stream_datetime.date().strftime('%m/%d/%Y'),
                        'time': streams[0].stream_datetime.time().strftime("%H:%M"),
                        'stream_name': streams[0].title,
                        'creator_name': f"{streams[0].creator.first_name} {streams[0].creator.last_name}"
                    }
                    send_templated_email(request.user.email, settings.USER_LIVE_STREAM_BOOKING_TEMPLATE, email_data)

                # Creator Email
                name = request.user.username if request.user.username else f"{request.user.first_name} {request.user.last_name}"
                email_data = {
                    'name': f"{streams[0].creator.first_name} {streams[0].creator.last_name}",
                    'user_name': name,
                    'date': streams[0].stream_datetime.date().strftime('%m/%d/%Y'),
                    'time': streams[0].stream_datetime.time().strftime("%H:%M"),
                    'stream_name': streams[0].title,
                    'cost': streams[0].stream_amount,
                    'seats_left': streams[0].total_seats - (check_seats.count())
                }
                send_templated_email(streams[0].creator.email, settings.CREATOR_LIVE_STREAM_BOOKING_TEMPLATE,
                                     email_data)

                return custom_response(True, status.HTTP_201_CREATED, message)
            else:
                message = chargeserializer.errors
                return custom_response(False, status.HTTP_400_BAD_REQUEST, message)

        except Exception as inst:
            print(inst)
            message = str(inst)
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)



class PayPalSessionBookingAPIView(APIView):
    """
    API View to book One to One Session through Paypal
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
            
            request_copy = request.data.copy()
            request_copy["user"] = request.user.pk

            chargeserializer = TransactionDetailSerializer(data=request_copy)
            if chargeserializer.is_valid():
                chargeserializer.save()
                print("<<<-----|| TransactionDetail CREATED ||----->>>")

                transaction = TransactionDetail.objects.filter(pk=chargeserializer.data['id'])

                session_booking = SessionBooking()
                session_booking.user = request.user
                session_booking.creator = check_booking[0].session.creator
                session_booking.time_slot = check_booking[0]
                session_booking.card_id = request.data['brand']
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
                notification_creator = Notification()
                notification_creator.notification_type= "BOOKING"
                notification_creator.user = check_booking[0].session.creator
                notification_creator.description = f"{request.user.username} booked one to one session with you on {check_booking[0].slot_datetime}"
                notification_creator.title = "Booking"
                notification_creator.profile_image = request.user.profile_image
                notification_creator.save()

                notification_user = Notification()
                notification_user.notification_type= "BOOKING"
                notification_user.user = request.user
                notification_user.title = "Booking"
                notification_user.profile_image = check_booking[0].session.creator.profile_image
                notification_user.description = f"Your one to one session with {check_booking[0].session.creator.first_name} {check_booking[0].session.creator.last_name} at {check_booking[0].slot_datetime} is booked successfully"
                notification_user.save()

                # User Email
                name = request.user.username if request.user.username else f"{request.user.first_name} {request.user.last_name}"
                if request.user.email:
                    email_data = {
                        'name': name,
                        'date': check_booking[0].slot_datetime.date().strftime('%m/%d/%Y'),
                        'time': check_booking[0].slot_datetime.time().strftime("%H:%M"),
                        'creator_name': f"{check_booking[0].session.creator.first_name} {check_booking[0].session.creator.last_name}"
                    }
                    send_templated_email(request.user.email, settings.USER_SESSION_BOOKING, email_data)

                # Creator Email
                name = request.user.username if request.user.username else f"{request.user.first_name} {request.user.last_name}"
                email_data = {
                    'name': f"{check_booking[0].session.creator.first_name} {check_booking[0].session.creator.last_name}",
                    'user_name': name,
                    'date': check_booking[0].slot_datetime.date().strftime('%m/%d/%Y'),
                    'time': check_booking[0].slot_datetime.time().strftime("%H:%M"),
                    'comments': session_booking.description,
                    'cost': check_booking[0].session.amount,
                }
                send_templated_email(check_booking[0].session.creator.email, settings.CREATOR_SESSION_BOOKING,
                                     email_data)

                return custom_response(True, status.HTTP_201_CREATED, message)
            else:
                message = chargeserializer.errors
                return custom_response(False, status.HTTP_400_BAD_REQUEST, message)

        except Exception as inst:
            print(inst)
            message = str(inst)
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)


class UserStreamListingAPIView(APIView):
    """
    Favourite Class
    """
    serializer_class = UserBookedStreamListingSerializer
    permission_classes = (IsAccountOwner, IsUser,)

    def get(self, request):
        booked_streams = StreamBooking.objects.filter(user=request.user.pk, stream__completed=False)
        message = "Stream Bookings fetched Successfully!"
        result = get_pagination_response(booked_streams, request, self.serializer_class, context = {"request": request})
        return custom_response(True, status.HTTP_200_OK, message, result)


class UserSessionListingAPIView(APIView):
    """
    Favourite Class
    """
    serializer_class = UserBookedSessionListingSerializer
    permission_classes = (IsAccountOwner, IsUser,)

    def get(self, request):
        booked_sessions = SessionBooking.objects.filter(user=request.user.pk, time_slot__completed=False)
        result = get_pagination_response(booked_sessions, request, self.serializer_class, context = {"request": request})
        message = "Session Bookings fetched Successfully!"
        return custom_response(True, status.HTTP_200_OK, message, result)