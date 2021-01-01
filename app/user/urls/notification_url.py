from django.urls import path
from . import views


urlpatterns = [

    path('notifications/', views.NotificationListView.as_view(), name='notification-list'),
    path('notification/read/', views.ReadAllNotificationView.as_view(), name='notifications-read-all'),
    path('notification/remove/', views.ReadAllNotificationView.as_view(), name='notifications-read-all'),
    path('notification/read/<int:pk>/', views.ReadNotificationView.as_view(), name='notification-read'),
]


