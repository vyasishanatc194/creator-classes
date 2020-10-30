# -*- coding: utf-8 -*-
from django.urls import include, path

from .. import views
from . import auth_url



urlpatterns = [
    path("", include(auth_url)),
]