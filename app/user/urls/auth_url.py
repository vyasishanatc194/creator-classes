from django.urls import path
from . import views


urlpatterns = [
    path("signup/", views.SignUpApiView.as_view(), name="signup"),
    path("login/", views.LoginAPIView.as_view(), name="login"),
    path("logout/", views.LogoutAPIView.as_view(), name="logout"),

    path('facebook/', views.FacebookLogin.as_view(), name='fb_login'),
    path('twitter/', views.TwitterLogin.as_view(), name='twitter_login'),
    path('google/', views.GoogleLogin.as_view(), name='google_login'),

    path('testimonials/', views.TestimonialsListingAPIView.as_view(), name='testimonials'),
    path('plans/', views.PlansListingAPIView.as_view(), name='plans'),
]


