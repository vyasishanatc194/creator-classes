from django.urls import path
from . import views


urlpatterns = [
    path("material-listing/", views.MaterialListingAPIView.as_view(), name="material-listing"),
]
