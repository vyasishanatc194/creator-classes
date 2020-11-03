from django.contrib.auth import views as auth_views
from django.urls import path, re_path, include
from django.conf.urls import url

from . import views

 
urlpatterns = [
    path("creator-review/", views.CreatorReviewAPIView.as_view(), name="add-creator-review"),
    path("creator-review/<int:pk>/", views.CreatorReviewAPIView.as_view(), name="creator-review"),
]


