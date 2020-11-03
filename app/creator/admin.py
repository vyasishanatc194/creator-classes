from django.contrib import admin
from .models import Creator, CreatorSkill, CreatorClass, ClassKeyword, ClassCovers

# Register your models here.


class CreatorAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ["pk", "email", "username",]


class CreatorSkillAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ["pk", "creator", "skill",]

class CreatorClassAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ["pk", "creator", "title",]

class ClassKeywordAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ["pk", "creator_class", "keyword",]

class ClassCoversAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ["pk", "creator_class", "covers",]


admin.site.register(Creator, CreatorAdmin)
admin.site.register(CreatorSkill, CreatorSkillAdmin)
admin.site.register(CreatorClass, CreatorClassAdmin)
admin.site.register(ClassKeyword, ClassKeywordAdmin)
admin.site.register(ClassCovers, ClassCoversAdmin)
    