from django.urls import path
from . import views


urlpatterns = [
    path("stream/", views.AddStreamAPIView.as_view(), name="add-stream"),

]