from django.urls import path
from . import views

app_name='customadmin'

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),

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
#------------------------------------------------------------------------------------------------------
    path("creator_export_product_csv", views.creator_export_product_csv, name="creator_export_product_csv"),
    
    path("creators/<int:pk>/detail/", views.CreatorDetailView.as_view(), name="creator-detailview"),
    path("creators/", views.CreatorListView.as_view(), name="creator-detail"),
    path("creators/", views.CreatorListView.as_view(), name="creator-list"),
    path("creators/create/", views.CreatorCreateView.as_view(), name="creator-create"),
    path("creators/<int:pk>/update/", views.CreatorUpdateView.as_view(), name="creator-update"),
    path("creators/<int:pk>/delete/", views.CreatorDeleteView.as_view(), name="creator-delete"),
    path("ajax-creators", views.CreatorAjaxPagination.as_view(), name="creator-list-ajax"),
    path("creators-accept/", views.CreatorAcceptRequestAjax, name="creator-accept"),
    path("creators-reject/", views.CreatorRejectRequestAjax, name="creator-reject"),
#------------------------------------------------------------------------------------------------------
    
    path("keywords/", views.AdminKeywordListView.as_view(), name="adminkeyword-detail"),
    path("keywords/", views.AdminKeywordListView.as_view(), name="adminkeyword-list"),
    path("keywords/create/", views.AdminKeywordCreateView.as_view(), name="adminkeyword-create"),
    path("keywords/<int:pk>/update/", views.AdminKeywordUpdateView.as_view(), name="adminkeyword-update"),
    path("keywords/<int:pk>/delete/", views.AdminKeywordDeleteView.as_view(), name="adminkeyword-delete"),
    path("ajax-keywords", views.AdminKeywordAjaxPagination.as_view(), name="adminkeyword-list-ajax"),
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    path("classes/<int:pk>/detail/", views.ClassDetailView.as_view(), name="creatorclass-detailview"),

    path("classes/", views.CreatorClassListView.as_view(), name="creatorclass-detail"),
    path("classes/", views.CreatorClassListView.as_view(), name="creatorclass-list"),
    path("classes/create/", views.CreatorClassCreateView.as_view(), name="creatorclass-create"),
    path("classes/<int:pk>/update/", views.CreatorClassUpdateView.as_view(), name="creatorclass-update"),
    path("classes/<int:pk>/delete/", views.CreatorClassDeleteView.as_view(), name="creatorclass-delete"),
    path("ajax-classes", views.CreatorClassAjaxPagination.as_view(), name="creatorclass-list-ajax"),
    path("get-materials/", views.GetMaterials, name="creatorclass-get-materials"),
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

    path("streams/<int:pk>/detail/", views.StreamDetailView.as_view(), name="stream-detailview"),
    path("streams/", views.StreamListView.as_view(), name="stream-detail"),
    path("streams/", views.StreamListView.as_view(), name="stream-list"),
    path("streams/create/", views.StreamCreateView.as_view(), name="stream-create"),
    path("streams/<int:pk>/update/", views.StreamUpdateView.as_view(), name="stream-update"),
    path("streams/<int:pk>/delete/", views.StreamDeleteView.as_view(), name="stream-delete"),
    path("ajax-streams", views.StreamAjaxPagination.as_view(), name="stream-list-ajax"),
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
    path("material/<int:pk>/detail/", views.MaterialDetailView.as_view(), name="material-detailview"),
    
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
#------------------------------------------------------------------------------------------------------
    
    path("one-to-one-sessions/", views.OneToOneSessionListView.as_view(), name="onetoonesession-detail"),
    path("one-to-one-sessions/", views.OneToOneSessionListView.as_view(), name="onetoonesession-list"),
    path("one-to-one-sessions/create/", views.OneToOneSessionCreateView.as_view(), name="onetoonesession-create"),
    path("one-to-one-sessions/<int:pk>/update/", views.OneToOneSessionUpdateView.as_view(), name="onetoonesession-update"),
    path("one-to-one-sessions/<int:pk>/delete/", views.OneToOneSessionDeleteView.as_view(), name="onetoonesession-delete"),
    path("ajax-one-to-one-sessions", views.OneToOneSessionAjaxPagination.as_view(), name="onetoonesession-list-ajax"),
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    path("plans/<int:pk>/detail/", views.PlanDetailView.as_view(), name="plan-detailview"),

    path("plans/", views.PlanListView.as_view(), name="plan-detail"),
    path("plans/", views.PlanListView.as_view(), name="plan-list"),
    path("plans/create/", views.PlanCreateView.as_view(), name="plan-create"),
    path("plans/<int:pk>/update/", views.PlanUpdateView.as_view(), name="plan-update"),
    path("plans/<int:pk>/delete/", views.PlanDeleteView.as_view(), name="plan-delete"),
    path("ajax-plans", views.PlanAjaxPagination.as_view(), name="plan-list-ajax"),
#------------------------------------------------------------------------------------------------------

]