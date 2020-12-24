from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import User, CreatorReview, ClassReview, SessionBooking, StreamBooking, FavouriteCreator, FavouriteClass
from .forms import AccountUpdateForm, AccountCreationForm
from django.utils.translation import ugettext_lazy as _


class UserAdmin(UserAdmin):
    form = AccountUpdateForm
    add_form = AccountCreationForm

    list_per_page = 10
    list_display = ["pk", "email", "username",]

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "username",
                    "profile_image",
                    "description",
                    "customer_id",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "password1",
                    "password2",
                    "profile_image",
                ),
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        instance = form.save(commit=False)
        instance.save()
        return instance


class CreatorReviewAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ["pk", "user", "creator", "rating"]


class ClassReviewAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ["pk", "user", "creator_class", "rating"]

class SessionBookingAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ["pk", "user", "creator", "time_slot"]
class StreamBookingAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ["pk", "user", "stream"]

class FavouriteCreatorAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ["pk"]

class FavouriteClassAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ["pk"]

admin.site.register(User, UserAdmin)
admin.site.register(CreatorReview, CreatorReviewAdmin)
admin.site.register(ClassReview, ClassReviewAdmin)
admin.site.register(SessionBooking, SessionBookingAdmin)
admin.site.register(StreamBooking, StreamBookingAdmin)
admin.site.register(FavouriteClass, FavouriteClassAdmin)
admin.site.register(FavouriteCreator, FavouriteCreatorAdmin)