from django.urls import path
from . import views


urlpatterns = [
    path("join-call/", views.JoinCallAPIView.as_view(), name="join-call"),
]
