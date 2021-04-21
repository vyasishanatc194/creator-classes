from rest_framework import fields, serializers
from ..models import Notification, User


class NotificationUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'profile_image')

class NotificationSerializer(serializers.ModelSerializer):
    user = NotificationUserSerializer()
    stream_start_time = serializers.SerializerMethodField()
    class Meta:
        model = Notification
        fields = ('id', 'title', 'description', 'user', 'notification_type', 'is_read', 'created_at','stream_start_time')

    def get_stream_start_time(self,instance):
        if instance.stream:
            return instance.stream.stream_datetime
        return None
