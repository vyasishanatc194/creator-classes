from rest_framework import fields, serializers
from user.models import StreamBooking, SessionBooking, UserPlanPurchaseHistory
from user.serializers import UserProfileUpdateSerializer
from ..models import Stream, OneToOneSession, CreatorTransferredMoney
from customadmin.models import CreatorClassCommission


creator_class_commission = CreatorClassCommission.objects.all()
if not creator_class_commission:
    creator_class_commission = CreatorClassCommission()
    creator_class_commission.affiliation_deduction = 10
    creator_class_commission.creator_class_deduction = 10
    creator_class_commission.save()



class StreamEarningSerializer(serializers.ModelSerializer):
    """
    Stream Earning serializer
    """ 
    creator_amount = serializers.SerializerMethodField()

    class Meta:
        model = Stream
        fields = ['id', 'title', 'stream_datetime', 'stream_amount', 'creator_amount']

    def get_creator_amount(self, instance):
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
        return instance.transaction_detail.brand

    def get_session_amount(self, instance):
        return instance.transaction_detail.amount

    def get_creator_session_amount(self, instance):
        amount = instance.transaction_detail.amount
        return amount - (amount * creator_class_commission.creator_class_deduction/100)


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
        return instance.plan_purchase_detail.amount

    def get_commission_amount(self, instance):
        plan_amount = instance.plan_purchase_detail.amount
        return (plan_amount * (creator_class_commission.affiliation_deduction/100))


class CreatorTransferredMoneyListingSerializer(serializers.ModelSerializer):

    class Meta:
        model = CreatorTransferredMoney
        fields = ['transaction_id', 'created_at', 'transferred_amount', 'affiliation_commission_total', 'stream_amount_received', 'session_amount_received']


