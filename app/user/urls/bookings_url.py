from django.urls import path
from . import views


urlpatterns = [
    path("session-booking/", views.OneToOneSessionBookingAPIView.as_view(), name="session-booking"),
]
