from django.contrib.auth import views as auth_views
from django.urls import path, re_path, include
from django.conf.urls import url

from . import views

 
urlpatterns = [
    path("favourite-class/<int:pk>/", views.FavouriteClassAPIView.as_view(), name="favourite-class"),
    path("favourite-class/", views.FavouriteClassAPIView.as_view(), name="favourite-class"),

    path("favourite-creator/<int:pk>/", views.FavouriteCreatorAPIView.as_view(), name="favourite-creator"),
    path("favourite-creator/", views.FavouriteCreatorAPIView.as_view(), name="favourite-creator"),
]
