from django.urls import path
from . import views


urlpatterns = [
    path("profile/", views.CreatorProfileAPI.as_view(), name="creator-profile"),

    path("creator-list/", views.CreatorListingAPIView.as_view(), name="creator-list"),
]