from django.urls import path
from . import views


urlpatterns = [
    path("total-earnings/", views.CreatorTotalEarningHistoryAPIView.as_view(), name="total-earnings"),
    path("affiliation-earnings-chart/", views.AffiliationEarningChartAPIView.as_view(), name="affiliation-earnings-chart"),
    path("stream-earnings-chart/", views.StreamEarningChartAPIView.as_view(), name="stream-earnings-chart"),
    path("session-earnings-chart/", views.CreatorSessionEarningChartAPIView.as_view(), name="session-earnings-chart"),

    path("stream-user-listing/", views.StreamUserListingAPIView.as_view(), name="stream-user-listing"),
    path("session-user-listing/", views.SessionUserListingAPIView.as_view(), name="session-user-listing"),
    path("affiliate-user-listing/", views.AffiliationUsersDetailAPIView.as_view(), name="affiliate-user-listing"),
]

