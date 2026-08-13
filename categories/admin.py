from django.contrib import admin

from .models import ServiceCategory



@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug","service_image", "base_price", "is_active"]
    prepopulated_fields = {"slug": ("name",)}
