from django.contrib.auth import views as auth_views
from django.urls import path, re_path, include
from django.conf.urls import url

from . import views


urlpatterns = [
    path("profile/", views.CreatorProfileAPI.as_view(), name="creator-profile"),
    
    path("creator-list/", views.CreatorListingAPIView.as_view(), name="creator-list"),
]


