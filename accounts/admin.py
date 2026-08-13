from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ["username", "email", "role", "phone_number", "city", "is_active"]
    list_filter = ["role", "is_active", "city"]
    fieldsets = UserAdmin.fieldsets + (
        ("Extra info", {"fields": ("role", "phone_number", "address", "city", "latitude", "longitude", "is_phone_verified")}),
    )
