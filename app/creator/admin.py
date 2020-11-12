from django.contrib import admin
from .models import Creator, CreatorSkill, CreatorClass, ClassKeyword, ClassCovers, ClassMaterial, Material, MaterialCategory, OneToOneSession, TimeSlot

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

class ClassMaterialAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ["pk", "creator_class", "class_material",]

class MaterialAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ["pk", "creator", "material_category", "title"]

class MaterialCategoryAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ["pk", "category_title", "created_at",]

class OneToOneSessionAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ["pk", "creator", "amount",]

class TimeSlotAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ["pk", "session", "slot_datetime", "is_booked",]


admin.site.register(Creator, CreatorAdmin)
admin.site.register(CreatorSkill, CreatorSkillAdmin)
admin.site.register(CreatorClass, CreatorClassAdmin)
admin.site.register(ClassKeyword, ClassKeywordAdmin)
admin.site.register(ClassCovers, ClassCoversAdmin)
admin.site.register(ClassMaterial, ClassMaterialAdmin)
admin.site.register(Material, MaterialAdmin)
admin.site.register(MaterialCategory, MaterialCategoryAdmin)
admin.site.register(OneToOneSession, OneToOneSessionAdmin)
admin.site.register(TimeSlot, TimeSlotAdmin)
    
