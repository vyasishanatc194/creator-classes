# -*- coding: utf-8 -*-
from django.urls import include, path

from .. import views
from . import auth_url, review_url, favourite_url, user_class_url, user_stream_url, card_url, user_material_url, bookings_url, notification_url

app_name="user"

urlpatterns = [
    path("", include(auth_url)),
    path("", include(review_url)),
    path("", include(favourite_url)),
    path("", include(user_class_url)),
    path("", include(user_stream_url)),
    path("", include(card_url)),
    path("", include(user_material_url)),
    path("", include(bookings_url)),
    path("", include(notification_url)),
]