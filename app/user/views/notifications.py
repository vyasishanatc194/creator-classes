from rest_framework.views import APIView
from ..serializers import NotificationSerializer
from ..models import Notification
from creator_class.helpers import custom_response, serialized_response, get_object
from rest_framework import status
from creator_class.permissions import IsAccountOwner


class NotificationListView(APIView):
    """
    Fetch all notifications of given user
    """
    permission_classes = (IsAccountOwner,)
    serializer_class = NotificationSerializer

    def get(self, request):
        notifications = Notification.objects.filter(user=request.user.pk).order_by('-id')
        serializer = self.serializer_class(notifications, many=True, context= {"request": request})
        message = "Notifications fetched successfully!"
        return custom_response(True, status.HTTP_200_OK, message, serializer.data)


class ReadAllNotificationView(APIView):
    """
    Mark all Notifications as read
    """
    permission_classes = (IsAccountOwner,)
    
    def post(self, request, format=None):
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        message = "All Notifications Marked as Read Successfully!"            
        return custom_response(True, status.HTTP_200_OK, message)


class RemoveAllNotificationView(APIView):
    """
    Mark all Notifications as read
    """
    permission_classes = (IsAccountOwner,)
    
    def delete(self, request, format=None):
        Notification.objects.filter(user=request.user).delete()
        message = "All Notifications removed Successfully!"            
        return custom_response(True, status.HTTP_200_OK, message)



class ReadNotificationView(APIView):
    """
    Mark given Notifications as read
    """
    
    permission_classes = (IsAccountOwner,)

    def post(self, request, pk, format=None):
        notification = get_object(Notification, pk)
        if not notification:
            message = "Notification not found!"
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)
        notification.is_read = True
        notification.save()
        message = "Notification Marked as Read Successfully!"
        return custom_response(True, status.HTTP_200_OK, message)

    def delete(self, request, pk, format=None):
        notification = get_object(Notification, pk)
        if not notification:
            message = "Notification not found!"
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)
        notification.delete()
        message = "Notification Deleted Successfully!"
        return custom_response(True, status.HTTP_200_OK, message)