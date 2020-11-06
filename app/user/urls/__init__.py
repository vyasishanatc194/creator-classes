# -*- coding: utf-8 -*-
from django.urls import include, path

from .. import views
from . import auth_url, review_url, favourite_url

app_name="user"

urlpatterns = [
    path("", include(auth_url)),
    path("", include(review_url)),
    path("", include(favourite_url)),
]