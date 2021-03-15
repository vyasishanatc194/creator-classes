from django.urls import path
from . import views
from django.conf.urls import url, include
from agora.views import Agora


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

    url(r'^dj-rest-auth/', include('dj_rest_auth.urls')),
    path('accounts/', include('allauth.urls')),

    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),

    path("forgot-password/", views.ForgotPasswordAPIView.as_view(), name="forgot-password"),
    path("set-password/", views.SetPasswordAPIView.as_view(), name="set-password"),
    
    path("cancel-subscription/", views.CancelSubscriptionAPIView.as_view(), name="calcel-subscription"),
    path("paypal-subscription/", views.PayPalPlanPurchaseAPIView.as_view(), name="paypal-subscription"),
    
    path("change-subscription/", views.ChangePlanAPIView.as_view(), name="change-subscription"),

    path("select-keywords/", views.UserSelectedKeywordsAPIView.as_view(), name="select-keywords"),
    path("select-keywords/", views.UserSelectedKeywordsAPIView.as_view(), name="select-keywords"),

    path('agora/',Agora.as_view(app_id='<APP_ID>', channel='<CHANNEL_ID>'
)),
]


