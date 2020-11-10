from django.contrib.auth import views as auth_views
from django.urls import path, re_path, include
from django.conf.urls import url

from . import views


urlpatterns = [
    path("material-category/", views.MaterialcategoryListingAPIView.as_view(), name="material-category"),
    path("material/", views.AddMaterialAPIView.as_view(), name="material"),
    path("material/<int:pk>/", views.AddMaterialAPIView.as_view(), name="material"),
    path("my-materials/", views.MyMaterialAPIView.as_view(), name="my-materials"),
]


