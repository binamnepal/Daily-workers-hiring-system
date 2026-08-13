"""
Business logic for browsing and managing service categories.
"""
from django.core.exceptions import ValidationError

from .models import ServiceCategory


class CategoryService:

    @staticmethod
    def list_active():
        return ServiceCategory.objects.filter(is_active=True)

    @staticmethod
    def get_by_slug(slug):
        try:
            return ServiceCategory.objects.get(slug=slug, is_active=True)
        except ServiceCategory.DoesNotExist:
            raise ValidationError(f"No active service category with slug '{slug}'.")

    @staticmethod
    def create_category(*, name, slug, description="", icon="", base_price):
        if ServiceCategory.objects.filter(slug=slug).exists():
            raise ValidationError("A category with this slug already exists.")
        return ServiceCategory.objects.create(
            name=name, slug=slug, description=description, icon=icon, base_price=base_price
        )

    @staticmethod
    def deactivate(category):
        category.is_active = False
        category.save(update_fields=["is_active"])
        return category
