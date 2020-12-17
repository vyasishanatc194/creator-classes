from django.urls import path
from . import views


urlpatterns = [
    path("stream/", views.AddStreamAPIView.as_view(), name="add-stream"),
    path("stream/<int:pk>/", views.AddStreamAPIView.as_view(), name="edit-stream"),
    path("my-streams/", views.MyStreamListingAPIView.as_view(), name="edit-stream"),
    path("creator-streams/", views.CreatorStreamListingAPIView.as_view(), name="creator-stream"),


]