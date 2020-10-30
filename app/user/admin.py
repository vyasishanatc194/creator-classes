from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import User
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


admin.site.register(User, UserAdmin)