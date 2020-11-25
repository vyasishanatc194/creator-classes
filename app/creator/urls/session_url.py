from django.urls import path
from . import views


urlpatterns = [
    path("session/", views.OneToOneSessionAPIView.as_view(), name="add-session"),
    path("sessions-list/<int:pk>/", views.CreatorSessionListingAPIView.as_view(), name="add-session"),
    path("my-sessions/", views.OneToOneSessionAPIView.as_view(), name="add-sessions"),
]