from django.urls import path
from . import views


urlpatterns = [
    path("stripe-connect/", views.StripeAccountConnectAPI.as_view(), name="stripe-connect"),
    path("stripe-disconnect/", views.StripeAccountDiscoonectAPI.as_view(), name="stripe-disconnect"),
    path("check-stripe-connect/", views.CheckStripeConnectAPIView.as_view(), name="check-stripe-connect"),

]