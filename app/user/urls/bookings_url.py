from django.urls import path
from . import views


urlpatterns = [
    path("book-session/", views.OneToOneSessionBookingAPIView.as_view(), name="book-session"),
]
