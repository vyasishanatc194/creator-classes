# -*- coding: utf-8 -*-
from django.urls import include, path

from .. import views
from . import auth_url, review_url



urlpatterns = [
    path("", include(auth_url)),
    path("", include(review_url)),
]