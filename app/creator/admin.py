from django.contrib import admin
from .models import Creator, CreatorSkill

# Register your models here.


class CreatorAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ["pk", "email", "username",]


class CreatorSkillAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ["pk", "creator", "skill",]


admin.site.register(Creator, CreatorAdmin)
admin.site.register(CreatorSkill, CreatorSkillAdmin)
    