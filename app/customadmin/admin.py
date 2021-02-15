from django.contrib import admin
from .models import Testimonial, AdminKeyword, Plan, PlanCover, AvailableTimezone

# Register your models here.
class TestimonialAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ["pk", "name", "email",]

admin.site.register(Testimonial, TestimonialAdmin)

class AdminKeywordAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ["pk", "keyword",]


class AvailableTimezoneAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ["pk"]

admin.site.register(AdminKeyword, AdminKeywordAdmin)
admin.site.register(Plan)
admin.site.register(PlanCover)
admin.site.register(AvailableTimezone, AvailableTimezoneAdmin)
