from rest_framework.views import APIView
from ..serializers import CreatorProfileSerializer, CreatorProfileDisplaySerializer, CreatorListingSerializer, CreatorRegisterSerializer, CreatorLoginSerializer
from ..models import Creator
from user.models import User, StreamBooking, SessionBooking
from creator_class.helpers import custom_response, serialized_response, get_object
from rest_framework import status, parsers, renderers
from django.contrib.auth import authenticate, login, logout
from creator_class.permissions import IsAccountOwner, IsCreator
from django.db.models import Sum
import datetime
from dateutil.relativedelta import relativedelta
import calendar


class CreatorProfileAPI(APIView):
    """
    Creator Profile view
    """
    serializer_class = CreatorProfileSerializer
    permission_classes = (IsAccountOwner, IsCreator)

    def put(self, request, *args, **kwargs):
        creator_profile = get_object(Creator, request.user.pk)
        if not creator_profile:
            message = "Creator not found!"
            return custom_response(True, status.HTTP_200_OK, message)
        message = "Profile updated successfully!"
        serializer = self.serializer_class(creator_profile, data=request.data, partial=True, context={"request": request})
        response_status, result, message = serialized_response(serializer, message)
        status_code = status.HTTP_201_CREATED if response_status else status.HTTP_400_BAD_REQUEST
        return custom_response(response_status, status_code, message, result)

    def get(self, request):
        creator_profile = get_object(Creator, request.user.pk)
        if not creator_profile:
            message = "Requested account details not found!"
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)
        serializer = CreatorProfileDisplaySerializer(creator_profile, context={"request": request})
        message = "Creator Details fetched Successfully!"
        return custom_response(True, status.HTTP_200_OK, message, serializer.data)


class CreatorDetailAPIView(APIView):
    def get(self, request,pk):
        creator_profile = get_object(Creator, pk)
        if not creator_profile:
            message = "Requested account details not found!"
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)
        serializer = CreatorProfileDisplaySerializer(creator_profile, context={"request": request})
        message = "Creator Details fetched Successfully!"
        return custom_response(True, status.HTTP_200_OK, message, serializer.data)



class CreatorListingAPIView(APIView):
    """
    Creator Profile view
    """
    serializer_class = CreatorListingSerializer
    def get(self, request):
        creators = Creator.objects.filter(is_active=True)

        key_skill = request.GET.get('key_skill', None)
        exclude_creator = request.GET.get('exclude_creator', None)
        
        if exclude_creator:
            creators = creators.exclude(pk=exclude_creator)

        if key_skill:
            creators = creators.filter(key_skill__icontains=key_skill)

        serializer = self.serializer_class(creators, many=True, context={"request": request})
        message = "Creators fetched Successfully!"
        return custom_response(True, status.HTTP_200_OK, message, serializer.data)


class CreatorRegisterView(APIView):
    """
    Creator Register View
    """
    serializer_class = CreatorRegisterSerializer

    def post(self, request, *args, **kwargs):
        if 'email' in request.data:
            email_check = User.objects.filter(email=request.data['email']).distinct()
        if email_check.exists():
            return custom_response(False, status.HTTP_400_BAD_REQUEST, "Email already exists!")
        if 'username' in request.data:
            username_check = User.objects.filter(username=request.data['username']).distinct()
        if username_check.exists():
            return custom_response(False, status.HTTP_400_BAD_REQUEST, "Username already exists!")
        message = "Account registered successfully!"
        serializer = self.serializer_class(data=request.data, context={'request': request})
        response_status, result, message = serialized_response(serializer, message)
        status_code = status.HTTP_201_CREATED if response_status else status.HTTP_400_BAD_REQUEST
        # TODO Email
        return custom_response(response_status, status_code, message, result)



class CreatorLoginAPIView(APIView):
    """
    User Login View
    """
    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
        parsers.JSONParser,
    )
    renderer_classes = (renderers.JSONRenderer,)

    def post(self, request, format=None):
        email = request.data.get("email", None)
        password = request.data.get("password", None)

        if not email or not password:
            message = "Email and password is required"
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)
        
        creator_exist = Creator.objects.filter(email=email)
        if not creator_exist:
            message = "Email/password combination invalid"
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)
        
        if not creator_exist[0].check_password(password):
            message = "Email/password combination invalid"
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)        
        
        if not creator_exist[0].is_active:
            message = "Account is not activated by admin yet!"
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)
        login(request, creator_exist[0], backend='django.contrib.auth.backends.ModelBackend')
        serializer = CreatorLoginSerializer(creator_exist[0], context={'request':request})
        return custom_response(True, status.HTTP_200_OK, "Login Successful!", serializer.data)


class CreatorEarningHistoryAPIView(APIView):
    """
    Creator Earning History view
    """
    permission_classes = (IsAccountOwner, IsCreator)
    def get(self, request):
        creator = Creator.objects.get(pk=request.user.pk)

        result = {}
        streams_booked = StreamBooking.objects.filter(stream__creator=request.user.pk)
        stream_earnings=streams_booked.aggregate(Sum('stream__stream_amount'))['stream__stream_amount__sum']

        session_booked = SessionBooking.objects.filter(creator=request.user.pk)
        session_earnings=session_booked.aggregate(Sum('transaction_detail__amount'))['transaction_detail__amount__sum']

        time_now = datetime.datetime.now()
        time_now = time_now + relativedelta(months=1)
        chart_data={}
        for i in range(0,10):
            time_now = time_now - relativedelta(months=1)
            monthly_streams_booked = StreamBooking.objects.filter(stream__creator=request.user.pk, created_at__date__month=time_now.month, created_at__date__year=time_now.year)
            monthly_stream_earnings=monthly_streams_booked.aggregate(Sum('stream__stream_amount'))['stream__stream_amount__sum']

            monthly_session_booked = SessionBooking.objects.filter(creator=request.user.pk, created_at__date__month=time_now.month, created_at__date__year=time_now.year)
            monthly_session_earnings=monthly_session_booked.aggregate(Sum('transaction_detail__amount'))['transaction_detail__amount__sum']

            chart_data[calendar.month_name[time_now.month]] = (monthly_stream_earnings if monthly_stream_earnings else 0) + (monthly_session_earnings if monthly_session_earnings else 0)

        result['total_earnings'] = (stream_earnings if stream_earnings else 0) + (session_earnings if session_earnings else 0)
        result['labels'] = chart_data.keys()
        result['data'] = chart_data.values()
        message = "Creators Earnings fetched Successfully!"
        return custom_response(True, status.HTTP_200_OK, message, result)


class CreatorFundsAPIView(APIView):
    """
    Creator Earning History view
    """
    permission_classes = (IsAccountOwner, IsCreator)
    def get(self, request):
        result = {}
        streams_booked = StreamBooking.objects.filter(stream__creator=request.user.pk)
        stream_earnings=streams_booked.aggregate(Sum('stream__stream_amount'))['stream__stream_amount__sum']

        session_booked = SessionBooking.objects.filter(creator=request.user.pk)
        session_earnings=session_booked.aggregate(Sum('transaction_detail__amount'))['transaction_detail__amount__sum']

        result['total_earnings'] = (stream_earnings if stream_earnings else 0) + (session_earnings if session_earnings else 0)
        result['transfered_amount'] = 0
        result['amount_to_transfer'] = result['total_earnings'] - result['transfered_amount']
        message = "Creators Earnings fetched Successfully!"
        return custom_response(True, status.HTTP_200_OK, message, result)