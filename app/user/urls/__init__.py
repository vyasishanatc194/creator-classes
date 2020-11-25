# -*- coding: utf-8 -*-
from django.urls import include, path

from .. import views
from . import auth_url, review_url, favourite_url, user_class_url, user_stream_url

app_name="user"

urlpatterns = [
    path("", include(auth_url)),
    path("", include(review_url)),
    path("", include(favourite_url)),
    path("", include(user_class_url)),
    path("", include(user_stream_url)),
]