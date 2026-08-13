"""
Business logic for account creation, verification and profile management.
Views/serializers should call into this module rather than talking to the
User model directly, so validation and side-effects (OTP, notifications,
worker-profile creation) stay in one place.
"""
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import transaction

User = get_user_model()


class AccountService:

    @staticmethod
    @transaction.atomic
    def register_customer(*, username, email, password, phone_number, address="", city=""):
        if User.objects.filter(phone_number=phone_number).exists():
            raise ValidationError("An account with this phone number already exists.")

        user = User(
            username=username,
            email=email,
            phone_number=phone_number,
            address=address,
            city=city,
            role=User.Role.CUSTOMER,
        )
        user.set_password(password)
        user.full_clean(exclude=["id"])
        user.save()
        return user

    @staticmethod
    @transaction.atomic
    def register_worker(*, username, email, password, phone_number, city, skills, bio="", hourly_rate=None):
        """
        Creates the User (role=worker) and delegates the WorkerProfile creation
        to WorkerService, so this is the single entry point for worker signup.
        """
        from workers.services import WorkerService

        if User.objects.filter(phone_number=phone_number).exists():
            raise ValidationError("An account with this phone number already exists.")

        user = User(
            username=username,
            email=email,
            phone_number=phone_number,
            city=city,
            role=User.Role.WORKER,
        )
        user.set_password(password)
        user.full_clean(exclude=["id"])
        user.save()

        WorkerService.create_profile(
            user=user, skills=skills, bio=bio, hourly_rate=hourly_rate, city=city
        )
        return user

    @staticmethod
    def update_location(*, user, latitude, longitude, address=""):
        user.latitude = latitude
        user.longitude = longitude
        if address:
            user.address = address
        user.save(update_fields=["latitude", "longitude", "address", "updated_at"])
        return user

    @staticmethod
    def verify_phone(*, user):
        user.is_phone_verified = True
        user.save(update_fields=["is_phone_verified", "updated_at"])
        return user
