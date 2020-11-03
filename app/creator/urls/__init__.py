# -*- coding: utf-8 -*-
from django.urls import include, path

from .. import views
from . import creator_url



urlpatterns = [
    path("", include(creator_url)),
]