from django.urls import path
from . import views


urlpatterns = [
    path("stream-detail/<int:pk>/", views.StreamDetailView.as_view(), name="stream-detail"),
    path("stream-search/", views.StreamSearchAPIView.as_view(), name="stream-search"),
]
