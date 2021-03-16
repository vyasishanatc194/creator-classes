from django.urls import path
from . import views


urlpatterns = [
    path("channel-token/", views.GenerateAgoraTokenAPIView.as_view(), name="channel-token"),
    path("session-screen-share/<int:pk>/", views.SessionScreenShareAPIView.as_view(), name="session-screen-share"),
    path("end-call/", views.EndCallAPIView.as_view(), name="end-call"),

]