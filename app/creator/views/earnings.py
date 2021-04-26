from rest_framework.views import APIView
from ..models import Creator, CreatorAffiliation, CreatorTransferredMoney
from user.models import User, StreamBooking, SessionBooking, UserPlanPurchaseHistory
from creator_class.helpers import custom_response, serialized_response
from rest_framework import status
from creator_class.permissions import IsAccountOwner, IsCreator, get_pagination_response
from django.db.models import Sum, Q
import datetime
from dateutil.relativedelta import relativedelta
import calendar
from customadmin.models import CreatorClassCommission
from ..serializers import StreamUserListingSerializer, SessionUserListingSerializer, UserPlanPurchaseHistorySerializer, CreatorTransferredMoneyListingSerializer
from creator_class.helpers import get_pagination_response


creator_class_commission = CreatorClassCommission.objects.all().first()
if not creator_class_commission:
    creator_class_commission = CreatorClassCommission()
    creator_class_commission.affiliation_deduction = 10
    creator_class_commission.creator_class_deduction = 10
    creator_class_commission.save()



class CreatorTotalEarningHistoryAPIView(APIView):
    """
    Creator Earning History view
    """

    permission_classes = (IsAccountOwner, IsCreator)

    def get(self, request):
        result = {}
        streams_booked = StreamBooking.objects.filter(stream__creator=request.user.pk)
        stream_earnings = streams_booked.aggregate(Sum("stream__stream_amount"))[
            "stream__stream_amount__sum"
        ]
        stream_earnings = (
            stream_earnings
            - (stream_earnings * creator_class_commission.creator_class_deduction / 100)
            if stream_earnings
            else 0
        )
        session_booked = SessionBooking.objects.filter(creator=request.user.pk)
        session_earnings = session_booked.aggregate(Sum("transaction_detail__amount"))[
            "transaction_detail__amount__sum"
        ]
        session_earnings = (
            session_earnings
            - (
                session_earnings
                * creator_class_commission.creator_class_deduction
                / 100
            )
            if session_earnings
            else 0
        )
        time_now = datetime.datetime.now()
        time_now = time_now + relativedelta(months=1)
        stream_chart = {}
        session_chart = {}
        affiliation_chart = {}
        for i in range(0, 10):
            time_now = time_now - relativedelta(months=1)
            monthly_streams_booked = streams_booked.filter(
                created_at__date__month=time_now.month,
                created_at__date__year=time_now.year,
            )
            monthly_stream_earnings = monthly_streams_booked.aggregate(
                Sum("stream__stream_amount")
            )["stream__stream_amount__sum"]

            month_stream_earnings = (
                monthly_stream_earnings
                - (
                    monthly_stream_earnings
                    * creator_class_commission.creator_class_deduction
                    / 100
                )
                if monthly_stream_earnings
                else 0
            )

            monthly_session_booked = session_booked.filter(
                created_at__date__month=time_now.month,
                created_at__date__year=time_now.year,
            )
            monthly_session_earnings = monthly_session_booked.aggregate(
                Sum("transaction_detail__amount")
            )["transaction_detail__amount__sum"]

            month_session_earnings = (
                monthly_session_earnings
                - (
                    monthly_session_earnings
                    * creator_class_commission.creator_class_deduction
                    / 100
                )
                if monthly_session_earnings
                else 0
            )

            stream_chart[calendar.month_name[time_now.month]] = (
                month_stream_earnings if month_stream_earnings else 0
            )

            session_chart[calendar.month_name[time_now.month]] = (
                month_session_earnings if month_session_earnings else 0
            )
            monthly_affiliation = CreatorAffiliation.objects.filter(
                user__affiliated_with=request.user.pk,
                created_at__date__month=time_now.month,
                created_at__date__year=time_now.year,
            )
            monthly_affiliation_earnings = monthly_affiliation.aggregate(
                Sum("commission_amount")
            )["commission_amount__sum"]

            affiliation_chart[calendar.month_name[time_now.month]] = (
                monthly_affiliation_earnings if monthly_affiliation_earnings else 0
            )

        # Total affiliation earnings
        affiliations = CreatorAffiliation.objects.filter(
            user__affiliated_with=request.user.pk
        )
        final_commission_amount = affiliations.aggregate(Sum("commission_amount"))[
            "commission_amount__sum"
        ]

        # Total earnings
        result["total_earnings"] = (
            (stream_earnings if stream_earnings else 0)
            + (session_earnings if session_earnings else 0)
            + (final_commission_amount if final_commission_amount else 0)
        )

        # This month total earnings
        this_month = datetime.datetime.now()
        this_month = this_month.date().month
        month_streams_booked = streams_booked.filter(
            stream__creator=request.user.pk, created_at__date__month=this_month
        )
        month_stream_earnings = month_streams_booked.aggregate(
            Sum("stream__stream_amount")
        )["stream__stream_amount__sum"]
        month_stream_earnings = (
            month_stream_earnings
            - (
                month_stream_earnings
                * creator_class_commission.creator_class_deduction
                / 100
            )
            if month_stream_earnings
            else 0
        )

        month_session_booked = session_booked.filter(
            creator=request.user.pk, created_at__date__month=this_month
        )
        month_session_earnings = month_session_booked.aggregate(
            Sum("transaction_detail__amount")
        )["transaction_detail__amount__sum"]
        month_session_earnings = (
            month_session_earnings
            - (
                month_session_earnings
                * creator_class_commission.creator_class_deduction
                / 100
            )
            if month_session_earnings
            else 0
        )

        month_affiliations = CreatorAffiliation.objects.filter(
            user__affiliated_with=request.user.pk, created_at__date__month=this_month
        )
        month_commission_amount = month_affiliations.aggregate(
            Sum("commission_amount")
        )["commission_amount__sum"]

        result["this_month_earnings"] = (
            (month_stream_earnings if month_stream_earnings else 0)
            + (month_session_earnings if month_session_earnings else 0)
            + (month_commission_amount if month_commission_amount else 0)
        )
        result["total_stream_earnings"] = stream_earnings if stream_earnings else 0
        result["total_session_earnings"] = session_earnings if session_earnings else 0
        result["total_affiliation_earnings"] = (
            final_commission_amount if final_commission_amount else 0
        )
        result["labels"] = stream_chart.keys()
        result["stream_chart"] = stream_chart.values()
        result["session_chart"] = session_chart.values()
        result["affiliation_chart"] = affiliation_chart.values()
        message = "Creators Total Earnings fetched Successfully!"
        return custom_response(True, status.HTTP_200_OK, message, result)



class AffiliationEarningChartAPIView(APIView):
    """
    Creator Earning History view
    """

    permission_classes = (IsAccountOwner, IsCreator)

    def get(self, request):
        result = {}
        time_now = datetime.datetime.now()
        time_now = time_now + relativedelta(months=1)
        affiliation_chart = {}
        for i in range(0, 10):
            time_now = time_now - relativedelta(months=1)
            monthly_affiliation = CreatorAffiliation.objects.filter(
                user__affiliated_with=request.user.pk,
                created_at__date__month=time_now.month,
                created_at__date__year=time_now.year,
            )
            monthly_affiliation_earnings = monthly_affiliation.aggregate(
                Sum("commission_amount")
            )["commission_amount__sum"]

            affiliation_chart[calendar.month_name[time_now.month]] = (
                monthly_affiliation_earnings if monthly_affiliation_earnings else 0
            )

        # Total affiliation earnings
        affiliations = CreatorAffiliation.objects.filter(
            user__affiliated_with=request.user.pk
        )
        final_commission_amount = affiliations.aggregate(Sum("commission_amount"))[
            "commission_amount__sum"
        ]


        # This month total earnings
        this_month = datetime.datetime.now()
        this_month = this_month.date().month
       
        month_affiliations = CreatorAffiliation.objects.filter(
            user__affiliated_with=request.user.pk, created_at__date__month=this_month
        )
        month_commission_amount = month_affiliations.aggregate(
            Sum("commission_amount")
        )["commission_amount__sum"]

        result["this_month_earnings"] = month_commission_amount if month_commission_amount else 0
        result["total_affiliation_earnings"] = final_commission_amount if final_commission_amount else 0
        result["labels"] = affiliation_chart.keys()
        result["data"] = affiliation_chart.values()
        message = "Creators total Affiliation Earnings fetched Successfully!"
        return custom_response(True, status.HTTP_200_OK, message, result)


class StreamEarningChartAPIView(APIView):
    """
    Creator Earning History view
    """

    permission_classes = (IsAccountOwner, IsCreator)

    def get(self, request):
        result = {}
        streams_booked = StreamBooking.objects.filter(stream__creator=request.user.pk)
        stream_earnings = streams_booked.aggregate(Sum("stream__stream_amount"))[
            "stream__stream_amount__sum"
        ]
        stream_earnings = (
            stream_earnings
            - (stream_earnings * creator_class_commission.creator_class_deduction / 100)
            if stream_earnings
            else 0
        )
        
        time_now = datetime.datetime.now()
        time_now = time_now + relativedelta(months=1)
        stream_chart = {}
        for i in range(0, 10):
            time_now = time_now - relativedelta(months=1)
            monthly_streams_booked = streams_booked.filter(
                created_at__date__month=time_now.month,
                created_at__date__year=time_now.year,
            )
            monthly_stream_earnings = monthly_streams_booked.aggregate(
                Sum("stream__stream_amount")
            )["stream__stream_amount__sum"]

            month_stream_earnings = (
                monthly_stream_earnings
                - (
                    monthly_stream_earnings
                    * creator_class_commission.creator_class_deduction
                    / 100
                )
                if monthly_stream_earnings
                else 0
            )
            stream_chart[calendar.month_name[time_now.month]] = (
                month_stream_earnings if month_stream_earnings else 0
            )
        # Total earnings
        result["total_earnings"] = stream_earnings if stream_earnings else 0         

        # This month total earnings
        this_month = datetime.datetime.now()
        this_month = this_month.date().month
        month_streams_booked = streams_booked.filter(
            stream__creator=request.user.pk, created_at__date__month=this_month
        )
        month_stream_earnings = month_streams_booked.aggregate(
            Sum("stream__stream_amount")
        )["stream__stream_amount__sum"]
        month_stream_earnings = (
            month_stream_earnings
            - (
                month_stream_earnings
                * creator_class_commission.creator_class_deduction
                / 100
            )
            if month_stream_earnings
            else 0
        )
       
        result["this_month_earnings"] = month_stream_earnings if month_stream_earnings else 0
        result["total_stream_earnings"] = stream_earnings if stream_earnings else 0
        result["labels"] = stream_chart.keys()
        result["stream_chart"] = stream_chart.values()
        message = "Creators total Stream earnings fetched Successfully!"
        return custom_response(True, status.HTTP_200_OK, message, result)


class CreatorSessionEarningChartAPIView(APIView):
    """
    Creator Session Earning History view
    """

    permission_classes = (IsAccountOwner, IsCreator)

    def get(self, request):
        result = {}
        session_booked = SessionBooking.objects.filter(creator=request.user.pk)
        session_earnings = session_booked.aggregate(Sum("transaction_detail__amount"))[
            "transaction_detail__amount__sum"
        ]
        session_earnings = (
            session_earnings
            - (
                session_earnings
                * creator_class_commission.creator_class_deduction
                / 100
            )
            if session_earnings
            else 0
        )
        time_now = datetime.datetime.now()
        time_now = time_now + relativedelta(months=1)
        session_chart = {}
        for i in range(0, 10):
            time_now = time_now - relativedelta(months=1)
            monthly_session_booked = session_booked.filter(
                created_at__date__month=time_now.month,
                created_at__date__year=time_now.year,
            )
            monthly_session_earnings = monthly_session_booked.aggregate(
                Sum("transaction_detail__amount")
            )["transaction_detail__amount__sum"]

            month_session_earnings = (
                monthly_session_earnings
                - (
                    monthly_session_earnings
                    * creator_class_commission.creator_class_deduction
                    / 100
                )
                if monthly_session_earnings
                else 0
            )
            session_chart[calendar.month_name[time_now.month]] = (
                month_session_earnings if month_session_earnings else 0
            )

        # This month total earnings
        this_month = datetime.datetime.now()
        this_month = this_month.date().month
        
        month_session_booked = session_booked.filter(
            creator=request.user.pk, created_at__date__month=this_month
        )
        month_session_earnings = month_session_booked.aggregate(
            Sum("transaction_detail__amount")
        )["transaction_detail__amount__sum"]
        month_session_earnings = (
            month_session_earnings
            - (
                month_session_earnings
                * creator_class_commission.creator_class_deduction
                / 100
            )
            if month_session_earnings
            else 0
        )

        result["this_month_earnings"] = month_session_earnings if month_session_earnings else 0
        result["total_session_earnings"] = session_earnings if session_earnings else 0
        result["labels"] = session_chart.keys()
        result["session_chart"] = session_chart.values()
        message = "Creators Total Session Earnings fetched Successfully!"
        return custom_response(True, status.HTTP_200_OK, message, result)


class StreamUserListingAPIView(APIView):
    """
    My class listing view
    """
    serializer_class = StreamUserListingSerializer
    permission_classes = (IsAccountOwner, IsCreator)

    def get(self, request):
        stream_bookings = StreamBooking.objects.filter(stream__creator=request.user.pk)

        start_date  = request.GET.get('start_date', None)
        end_date  = request.GET.get('end_date', None)
        search  = request.GET.get('search', None)

        if start_date:
            stream_bookings = stream_bookings.filter(created_at__date__gte=start_date)
        
        if end_date:
            stream_bookings = stream_bookings.filter(created_at__date__lte=end_date)

        if search:
            search_bookings = stream_bookings.filter(Q(transaction_detail__brand__icontains=search) | Q(user__username__icontains=search) |Q(user__first_name__icontains=search) |Q(user__last_name__icontains=search) | Q(created_at__date__icontains=search))
            booking_list = []
            for booking in search_bookings:
                booking_list.append(booking)
            for stream_booking in stream_bookings:
                creator_amount = stream_booking.stream.stream_amount - (stream_booking.stream.stream_amount * (creator_class_commission.creator_class_deduction)/100)
                if search in str(creator_amount):
                    if stream_booking not in booking_list:
                        booking_list.append(stream_booking)

            result = get_pagination_response(booking_list, request, self.serializer_class, context = {"request": request})
            message = "Booking detail fetched Successfully!"
            return custom_response(True, status.HTTP_200_OK, message, result)


        result = get_pagination_response(stream_bookings, request, self.serializer_class, context = {"request": request})
        message = "Booking detail fetched Successfully!"
        return custom_response(True, status.HTTP_200_OK, message, result)


class SessionUserListingAPIView(APIView):
    """
    My Session user listing view
    """
    serializer_class = SessionUserListingSerializer
    permission_classes = (IsAccountOwner, IsCreator)

    def get(self, request):
        session_bookings = SessionBooking.objects.filter(creator=request.user.pk)

        start_date  = request.GET.get('start_date', None)
        end_date  = request.GET.get('end_date', None)
        search  = request.GET.get('search', None)

        if start_date:
            session_bookings = session_bookings.filter(created_at__date__gte=start_date)
        
        if end_date:
            session_bookings = session_bookings.filter(created_at__date__lte=end_date)

        if search:
            search_bookings = session_bookings.filter(Q(transaction_detail__brand__icontains=search) | Q(user__username__icontains=search)|Q(user__first_name__icontains=search) |Q(user__last_name__icontains=search) | Q(created_at__date__icontains=search))
            booking_list = []
            for booking in search_bookings:
                booking_list.append(booking)

            for session_booking in session_bookings:
                creator_amount = session_booking.transaction_detail.amount - (session_booking.transaction_detail.amount * (creator_class_commission.creator_class_deduction)/100)
                if search in str(creator_amount):
                    if session_booking not in booking_list:
                        booking_list.append(session_booking)

            result = get_pagination_response(booking_list, request, self.serializer_class, context = {"request": request})
            message = "Booking detail fetched Successfully!"
            return custom_response(True, status.HTTP_200_OK, message, result)

        result = get_pagination_response(session_bookings, request, self.serializer_class, context = {"request": request})
        message = "Booking detail fetched Successfully!"
        return custom_response(True, status.HTTP_200_OK, message, result)


class AffiliationUsersDetailAPIView(APIView):
    """
    Affiliated users detail listing API View
    """

    permission_classes = (IsAccountOwner, IsCreator)
    serializer_class = UserPlanPurchaseHistorySerializer

    def get(self, request):
        plans_purchased = UserPlanPurchaseHistory.objects.filter(user__is_creator=False, user__affiliated_with=request.user.pk)
        start_date  = request.GET.get('start_date', None)
        end_date  = request.GET.get('end_date', None)
        search  = request.GET.get('search', None)

        if start_date:
            plans_purchased = plans_purchased.filter(created_at__date__gte=start_date)
        
        if end_date:
            plans_purchased = plans_purchased.filter(created_at__date__lte=end_date)

        if search:
            search_plans = plans_purchased.filter(Q(plan_purchase_detail__brand__icontains=search) | Q(user__username__icontains=search) |Q(user__first_name__icontains=search) |Q(user__last_name__icontains=search) | Q(created_at__date__icontains=search))
            plan_purchase_list = []
            for booking in search_plans:
                plan_purchase_list.append(booking)

            for plan in plans_purchased:
                if search in str(plan.plan_purchase_detail.amount):
                    if plan not in plan_purchase_list:
                        plan_purchase_list.append(plan)
                creator_amount = plan.plan_purchase_detail.amount * (creator_class_commission.affiliation_deduction)/100
                if search in str(creator_amount):
                    if plan not in plan_purchase_list:
                        plan_purchase_list.append(plan)

            result = get_pagination_response(plan_purchase_list, request, self.serializer_class, context = {"request": request})
            message = "Booking detail fetched Successfully!"
            return custom_response(True, status.HTTP_200_OK, message, result)

        result = get_pagination_response(
            plans_purchased, request, self.serializer_class, context={"request": request}
        )
        message = "Affiliated users fetched Successfully!"
        return custom_response(True, status.HTTP_200_OK, message, result)


class PayoutsDetailAPIView(APIView):
    """
    Affiliated users detail listing API View
    """

    permission_classes = (IsAccountOwner, IsCreator)
    serializer_class = CreatorTransferredMoneyListingSerializer

    def get(self, request):
        transactions = CreatorTransferredMoney.objects.filter(creator=request.user.pk)
        start_date  = request.GET.get('start_date', None)
        end_date  = request.GET.get('end_date', None)
        search  = request.GET.get('search', None)

        if start_date:
            transactions = transactions.filter(created_at__date__gte=start_date)
        
        if end_date:
            transactions = transactions.filter(created_at__date__lte=end_date)

        if search:
            transactions = transactions.filter(Q(transaction_id__icontains=search) | Q(transferred_amount__icontains=search) | Q(created_at__date__icontains=search))

        result = get_pagination_response(
            transactions, request, self.serializer_class, context={"request": request}
        )
        message = "Payouts fetched Successfully!"
        return custom_response(True, status.HTTP_200_OK, message, result)