from django.contrib import admin

# Register your models here.
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "username", "email"]
    list_per_page = 10


admin.site.register(User, UserAdmin)