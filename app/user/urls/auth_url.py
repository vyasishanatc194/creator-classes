from django.contrib.auth import views as auth_views
from django.urls import path, re_path, include
from django.conf.urls import url

from . import views

 
urlpatterns = [
    path("signup/", views.SignUpApiView.as_view(), name="signup"),
]


