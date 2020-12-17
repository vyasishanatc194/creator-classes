from django.urls import path
from . import views


urlpatterns = [
    path("material-category/", views.MaterialcategoryListingAPIView.as_view(), name="material-category"),
    path("material/", views.AddMaterialAPIView.as_view(), name="material"),
    path("material/<int:pk>/", views.AddMaterialAPIView.as_view(), name="material"),
    path("my-materials/", views.MyMaterialAPIView.as_view(), name="my-materials"),
    path("creator-material/", views.CreatorMaterialAPIView.as_view(), name="creator-materials"),
]
