from django.contrib.auth import views as auth_views
from django.urls import path, re_path, include
from django.conf.urls import url

from . import views

 
urlpatterns = [
    path("signup/", views.SignUpApiView.as_view(), name="signup"),
    path("login/", views.LoginAPIView.as_view(), name="login"),
    path("logout/", views.LogoutAPIView.as_view(), name="logout"),

    # url(r'^api/login/', include('rest_social_auth.urls_token')),

    # path('facebook/', views.FacebookLogin.as_view(), name='fb_login'),
    # path('twitter/', views.TwitterLogin.as_view(), name='twitter_login'),
    # path('google/', views.GoogleLogin.as_view(), name='google_login'),
]


