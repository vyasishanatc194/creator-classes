from django.urls import path
from . import views


urlpatterns = [
    path("card/", views.CardAPIView.as_view(), name="add-card"),
    path('card/<int:pk>/', views.CardAPIView.as_view(), name='card-update'),
    path('card-detail/<int:pk>/', views.CardDetailAPIView.as_view(), name='card-update'),
]
