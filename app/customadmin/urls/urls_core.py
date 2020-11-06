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
    
    path("creator-reviews/", views.CreatorReviewListView.as_view(), name="creatorreview-detail"),
    path("creator-reviews/", views.CreatorReviewListView.as_view(), name="creatorreview-list"),
    path("creator-reviews/create/", views.CreatorReviewCreateView.as_view(), name="creatorreview-create"),
    path("creator-reviews/<int:pk>/update/", views.CreatorReviewUpdateView.as_view(), name="creatorreview-update"),
    path("creator-reviews/<int:pk>/delete/", views.CreatorReviewDeleteView.as_view(), name="creatorreview-delete"),
    path("ajax-creator-reviews", views.CreatorReviewAjaxPagination.as_view(), name="creatorreview-list-ajax"),
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    
    path("class-reviews/", views.ClassReviewListView.as_view(), name="classreview-detail"),
    path("class-reviews/", views.ClassReviewListView.as_view(), name="classreview-list"),
    path("class-reviews/create/", views.ClassReviewCreateView.as_view(), name="classreview-create"),
    path("class-reviews/<int:pk>/update/", views.ClassReviewUpdateView.as_view(), name="classreview-update"),
    path("class-reviews/<int:pk>/delete/", views.ClassReviewDeleteView.as_view(), name="classreview-delete"),
    path("ajax-class-reviews", views.ClassReviewAjaxPagination.as_view(), name="classreview-list-ajax"),
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    
    path("material-category/", views.MaterialCategoryListView.as_view(), name="materialcategory-detail"),
    path("material-category/", views.MaterialCategoryListView.as_view(), name="materialcategory-list"),
    path("material-category/create/", views.MaterialCategoryCreateView.as_view(), name="materialcategory-create"),
    path("material-category/<int:pk>/update/", views.MaterialCategoryUpdateView.as_view(), name="materialcategory-update"),
    path("material-category/<int:pk>/delete/", views.MaterialCategoryDeleteView.as_view(), name="materialcategory-delete"),
    path("ajax-material-category", views.MaterialCategoryAjaxPagination.as_view(), name="materialcategory-list-ajax"),
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    
    path("material/", views.MaterialListView.as_view(), name="material-detail"),
    path("material/", views.MaterialListView.as_view(), name="material-list"),
    path("material/create/", views.MaterialCreateView.as_view(), name="material-create"),
    path("material/<int:pk>/update/", views.MaterialUpdateView.as_view(), name="material-update"),
    path("material/<int:pk>/delete/", views.MaterialDeleteView.as_view(), name="material-delete"),
    path("ajax-material", views.MaterialAjaxPagination.as_view(), name="material-list-ajax"),
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    
    path("testimonials/", views.TestimonialListView.as_view(), name="testimonial-detail"),
    path("testimonials/", views.TestimonialListView.as_view(), name="testimonial-list"),
    path("testimonials/create/", views.TestimonialCreateView.as_view(), name="testimonial-create"),
    path("testimonials/<int:pk>/update/", views.TestimonialUpdateView.as_view(), name="testimonial-update"),
    path("testimonials/<int:pk>/delete/", views.TestimonialDeleteView.as_view(), name="testimonial-delete"),
    path("ajax-testimonials", views.TestimonialAjaxPagination.as_view(), name="testimonial-list-ajax"),
#------------------------------------------------------------------------------------------------------

]