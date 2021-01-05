from django.urls import path
from . import views


urlpatterns = [
    path("signup/", views.SignUpApiView.as_view(), name="signup"),
    path("login/", views.LoginAPIView.as_view(), name="login"),
    path("logout/", views.LogoutAPIView.as_view(), name="logout"),

    path('rest-auth/facebook/', views.FacebookLogin.as_view(), name='fb_login'),
    path('rest-auth/google/', views.GoogleLogin.as_view(), name='google_login'),

    path('testimonials/', views.TestimonialsListingAPIView.as_view(), name='testimonials'),
    path('plans/', views.PlansListingAPIView.as_view(), name='plans'),
    path('profile/', views.UserProfileAPIView.as_view(), name='plans'),    
    path('purchase-plan/', views.PlanPurchaseAPIView.as_view(), name='purchase-plan'),
    path('user-plan/', views.UserPlanAPIView.as_view(), name='user-plan'),
]


