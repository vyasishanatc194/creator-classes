from django.urls import path
from . import views


urlpatterns = [
    path("creator-review/", views.CreatorReviewAPIView.as_view(), name="add-creator-review"),
    path("creator-review/<int:pk>/", views.CreatorReviewAPIView.as_view(), name="creator-review"),

    path("class-review/", views.ClassReviewAPIView.as_view(), name="add-class-review"),
    path("class-review/<int:pk>/", views.ClassReviewAPIView.as_view(), name="class-review"),
]
