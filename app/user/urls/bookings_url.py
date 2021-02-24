from django.urls import path
from . import views


urlpatterns = [
    path("book-session/", views.OneToOneSessionBookingAPIView.as_view(), name="book-session"),
    path("book-stream/", views.StreamBookingAPIView.as_view(), name="book-stream"),
    path("stream-seat-holders/<int:pk>/", views.StreamSeatHolderAPIView.as_view(), name="stream-seat-holders"),
    path("session-seat-holders/", views.BookedSessionSeatholdersAPIView.as_view(), name="session-seat-holders"),
    
    path("paypal-book-stream/", views.PayPalStreamBookingAPIView.as_view(), name="paypal-book-stream"),
]
