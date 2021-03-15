from django.urls import path
from . import views


urlpatterns = [
    path("book-session/", views.OneToOneSessionBookingAPIView.as_view(), name="book-session"),
    path("book-stream/", views.StreamBookingAPIView.as_view(), name="book-stream"),
    path("stream-seat-holders/<int:pk>/", views.StreamSeatHolderAPIView.as_view(), name="stream-seat-holders"),
    path("session-seat-holders/", views.BookedSessionSeatholdersAPIView.as_view(), name="session-seat-holders"),
    
    path("paypal-book-stream/", views.PayPalStreamBookingAPIView.as_view(), name="paypal-book-stream"),
    path("paypal-book-session/", views.PayPalSessionBookingAPIView.as_view(), name="paypal-book-session"),

    path("booked-streams/", views.UserStreamListingAPIView.as_view(), name="booked-streams"),
    path("booked-sessions/", views.UserSessionListingAPIView.as_view(), name="booked-sessions"),

]
