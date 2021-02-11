from rest_framework import fields, serializers
from user.models import StreamBooking
from user.serializers import UserProfileUpdateSerializer



class StreamUserListingSerializer(serializers.ModelSerializer):
    user = UserProfileUpdateSerializer()
    category_name = serializers.RelatedField(source='category', read_only=True)
    payment_method = serializers.SerializerMethodField()
    class Meta:
        model = StreamBooking
        fields = ['user', 'stream', 'transaction_detail', 'created_at', 'payment_method']

    def get_payment_method(self, instance):
        return instance.transaction_detail.brand