from django.contrib.auth import views as auth_views
from django.urls import path, re_path, include
from django.conf.urls import url

from . import views

 
urlpatterns = [
    path("class/", views.AddClassAPIView.as_view(), name="add-class"),
    path("class/<int:pk>/", views.AddClassAPIView.as_view(), name="update-class"),

    path("my-classes/", views.MyClassListingAPIView.as_view(), name="my-classes"),
    path("class-detail/<int:pk>/", views.ClassDetailAPIView.as_view(), name="class-detail"),

    path("keywords/", views.KeywordsAPIView.as_view(), name="class-detail"),

]