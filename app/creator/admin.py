from django.contrib import admin
from .models import Creator, CreatorSkill, CreatorClass, ClassKeyword, ClassCovers, Material, MaterialCategory, ClassMaterial, OneToOneSession

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

class MaterialAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ["pk", "creator", "material_category", "title"]

class MaterialCategoryAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ["pk", "category_title", "created_at",]


admin.site.register(Creator, CreatorAdmin)
admin.site.register(CreatorSkill, CreatorSkillAdmin)
admin.site.register(CreatorClass, CreatorClassAdmin)
admin.site.register(ClassKeyword, ClassKeywordAdmin)
admin.site.register(ClassCovers, ClassCoversAdmin)
admin.site.register(Material, MaterialAdmin)
admin.site.register(MaterialCategory, MaterialCategoryAdmin)
admin.site.register(ClassMaterial)
admin.site.register(OneToOneSession)