from rest_framework import fields, serializers
from user.models import StreamBooking, SessionBooking, UserPlanPurchaseHistory
from user.serializers import UserProfileUpdateSerializer
from ..models import Stream, OneToOneSession, CreatorTransferredMoney
from customadmin.models import CreatorClassCommission



class StreamEarningSerializer(serializers.ModelSerializer):
    """
    Stream Earning serializer
    """
    creator_amount = serializers.SerializerMethodField()

    class Meta:
        model = Stream
        fields = ['id', 'title', 'stream_datetime', 'stream_amount', 'creator_amount']

    def get_creator_amount(self, instance):
        creator_class_commission = CreatorClassCommission.objects.all().first()
        if not creator_class_commission:
            creator_class_commission = CreatorClassCommission()
            creator_class_commission.affiliation_deduction = 35
            creator_class_commission.creator_class_deduction = 20
            creator_class_commission.save()
        return instance.stream_amount - (instance.stream_amount * creator_class_commission.creator_class_deduction/100)


class StreamUserListingSerializer(serializers.ModelSerializer):
    user = UserProfileUpdateSerializer()
    payment_method = serializers.SerializerMethodField()
    stream = StreamEarningSerializer()
    class Meta:
        model = StreamBooking
        fields = ['user', 'stream', 'created_at', 'payment_method']

    def get_payment_method(self, instance):
        return instance.transaction_detail.brand



class SessionUserListingSerializer(serializers.ModelSerializer):
    user = UserProfileUpdateSerializer()
    payment_method = serializers.SerializerMethodField()
    session_amount = serializers.SerializerMethodField()
    creator_session_amount = serializers.SerializerMethodField()
    class Meta:
        model = SessionBooking
        fields = ['user', 'created_at', 'payment_method', 'session_amount', 'creator_session_amount']

    def get_payment_method(self, instance):
        if instance.transaction_detail:
            return instance.transaction_detail.brand
        return None

    def get_session_amount(self, instance):
        if instance.transaction_detail:
            amount = instance.transaction_detail.amount/100
            return float('%.2f'%amount)
        return 0

    def get_creator_session_amount(self, instance):
        creator_class_commission = CreatorClassCommission.objects.all().first()
        if not creator_class_commission:
            creator_class_commission = CreatorClassCommission()
            creator_class_commission.affiliation_deduction = 35
            creator_class_commission.creator_class_deduction = 20
            creator_class_commission.save()
        if instance.transaction_detail:
            amount = instance.transaction_detail.amount
            creator_amount = (amount - (amount * creator_class_commission.creator_class_deduction/100))/100
            return float('%.2f'%creator_amount)
        return 0


class UserPlanPurchaseHistorySerializer(serializers.ModelSerializer):
    user = UserProfileUpdateSerializer()
    payment_method = serializers.SerializerMethodField()
    plan_amount = serializers.SerializerMethodField()
    commission_amount = serializers.SerializerMethodField()

    class Meta:
        model = UserPlanPurchaseHistory
        fields = ['user', 'plan', 'created_at', 'payment_method', 'plan_amount', 'commission_amount']

    def get_payment_method(self, instance):
        return instance.plan_purchase_detail.brand

    def get_plan_amount(self, instance):
        amount = instance.plan_purchase_detail.amount/100
        return float('%.2f' %amount)

    def get_commission_amount(self, instance):
        creator_class_commission = CreatorClassCommission.objects.all().first()
        if not creator_class_commission:
            creator_class_commission = CreatorClassCommission()
            creator_class_commission.affiliation_deduction = 35
            creator_class_commission.creator_class_deduction = 20
            creator_class_commission.save()
        plan_amount = instance.plan_purchase_detail.amount
        if not plan_amount:
            plan_amount = 0
        amount = (plan_amount * (creator_class_commission.affiliation_deduction/100))/100
        return float('%.2f'%amount)


class CreatorTransferredMoneyListingSerializer(serializers.ModelSerializer):
    transferred_amount = serializers.SerializerMethodField()
    stream_amount_received = serializers.SerializerMethodField()
    session_amount_received = serializers.SerializerMethodField()

    class Meta:
        model = CreatorTransferredMoney
        fields = ['transaction_id', 'created_at', 'transferred_amount', 'affiliation_commission_total', 'stream_amount_received', 'session_amount_received']


    def get_transferred_amount(self, instance):
        return float('%.2f'%(instance.transferred_amount/100))


    def get_stream_amount_received(self, instance):
        return float('%.2f'%(instance.stream_amount_received/100))


    def get_session_amount_received(self, instance):
        return float('%.2f'%(instance.session_amount_received/100))

