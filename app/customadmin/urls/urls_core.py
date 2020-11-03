from django.urls import path, include
from django.views.generic import TemplateView
from . import views

app_name='customadmin'

urlpatterns = [
    
    path("", views.IndexView.as_view(), name="index"),

    # path("", TemplateView.as_view(template_name="core/home.html"), name="home"),

    # User
    path("users/", views.UserListView.as_view(), name="user-detail"),

    path("users/", views.UserListView.as_view(), name="user-list"),
    path("users/create/", views.UserCreateView.as_view(), name="user-create"),
    path("users/<int:pk>/update/", views.UserUpdateView.as_view(), name="user-update"),
    path("users/<int:pk>/delete/", views.UserDeleteView.as_view(), name="user-delete"),
    path("users/<int:pk>/password/", views.UserPasswordView.as_view(), name="user-password"),
    path("ajax-users", views.UserAjaxPagination.as_view(), name="user-list-ajax"),

    path("export_user_csv", views.export_user_csv, name="export_user_csv"),


]

urlpatterns +=[
#     # path("creators/", views.CreatorListView.as_view(), name="creator-list"),
    path("streams/", views.StreamListView.as_view(), name="stream-list"),


#------------------------------------------------------------------------------------------------------
    path("creator_export_product_csv", views.creator_export_product_csv, name="creator_export_product_csv"),
    
    path("creators/", views.CreatorListView.as_view(), name="creator-detail"),
    path("creators/", views.CreatorListView.as_view(), name="creator-list"),
    path("creators/create/", views.CreatorCreateView.as_view(), name="creator-create"),
    path("creators/<int:pk>/update/", views.CreatorUpdateView.as_view(), name="creator-update"),
    path("creators/<int:pk>/delete/", views.CreatorDeleteView.as_view(), name="creator-delete"),
    path("ajax-creators", views.CreatorAjaxPagination.as_view(), name="creator-list-ajax"),
#------------------------------------------------------------------------------------------------------
    
    path("classes/", views.CreatorClassListView.as_view(), name="creatorclass-detail"),
    path("classes/", views.CreatorClassListView.as_view(), name="creatorclass-list"),
    path("classes/create/", views.CreatorClassCreateView.as_view(), name="creatorclass-create"),
    path("classes/<int:pk>/update/", views.CreatorClassUpdateView.as_view(), name="creatorclass-update"),
    path("classes/<int:pk>/delete/", views.CreatorClassDeleteView.as_view(), name="creatorclass-delete"),
    path("ajax-classes", views.CreatorClassAjaxPagination.as_view(), name="creatorclass-list-ajax"),
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    
    path("reviews/", views.CreatorReviewListView.as_view(), name="creatorreview-detail"),
    path("reviews/", views.CreatorReviewListView.as_view(), name="creatorreview-list"),
    path("reviews/create/", views.CreatorReviewCreateView.as_view(), name="creatorreview-create"),
    path("reviews/<int:pk>/update/", views.CreatorReviewUpdateView.as_view(), name="creatorreview-update"),
    path("reviews/<int:pk>/delete/", views.CreatorReviewDeleteView.as_view(), name="creatorreview-delete"),
    path("ajax-reviews", views.CreatorReviewAjaxPagination.as_view(), name="creatorreview-list-ajax"),
#------------------------------------------------------------------------------------------------------

]