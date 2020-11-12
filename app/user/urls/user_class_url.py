from django.urls import path
from . import views


urlpatterns = [
    path("class-filter/", views.ClassFilterAPIView.as_view(), name="class-filter"),
    path("class-search/", views.ClassSearchAPIView.as_view(), name="class-filter"),
]
