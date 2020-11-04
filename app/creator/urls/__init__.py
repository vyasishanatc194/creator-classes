# -*- coding: utf-8 -*-
from django.urls import include, path

from .. import views
from . import creator_url, class_url

app_name = "creator"

urlpatterns = [
    path("", include(creator_url)),
    path("", include(class_url)),
]