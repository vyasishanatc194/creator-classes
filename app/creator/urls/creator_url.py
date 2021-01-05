from django.urls import path
from . import views


urlpatterns = [
    path("profile/", views.CreatorProfileAPI.as_view(), name="creator-profile"),

    path("creator-list/", views.CreatorListingAPIView.as_view(), name="creator-list"),

    path("register/", views.CreatorRegisterView.as_view(), name="register"),
    path("login/", views.CreatorLoginAPIView.as_view(), name="creator-login"),
    
    path("creator-detail/<int:pk>/", views.CreatorDetailAPIView.as_view(), name="creator-detail"),
    path("earning-history/", views.CreatorEarningHistoryAPIView.as_view(), name="earning-history"),
    path("funds-history/", views.CreatorFundsAPIView.as_view(), name="funds-history"),

]