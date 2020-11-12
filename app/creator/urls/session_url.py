from django.urls import path
from . import views


urlpatterns = [
    path("session/", views.OneToOneSessionAPIView.as_view(), name="add-session"),
]