from django.urls import path
from . import views

urlpatterns = [
path('get-country-list/', views.CountryListAPIView.as_view(), name='country-list'),
]