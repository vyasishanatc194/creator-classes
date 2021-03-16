# -*- coding: utf-8 -*-
from django.urls import include, path

from .. import views
from . import creator_url, class_url, material_url, session_url, stream_url, stripe_connect_url, earning_url, video_call_urls

app_name = "creator"

urlpatterns = [
    path("", include(creator_url)),
    path("", include(class_url)),
    path("", include(material_url)),
    path("", include(session_url)),
    path("", include(stream_url)),
    path("", include(stripe_connect_url)),
    path("", include(earning_url)),
    path("", include(video_call_urls)),
]