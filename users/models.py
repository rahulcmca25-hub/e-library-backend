from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):

        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(
            email=email,
            password=password,
            **extra_fields
        )


class User(AbstractUser):

    class Role(models.TextChoices):
        MEMBER = "MEMBER", "Member"
        LIBRARIAN = "LIBRARIAN", "Librarian"
        ADMIN = "ADMIN", "Admin"

    # Remove username because we are using email for login
    username = None

    email = models.EmailField(
        unique=True
    )

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.MEMBER
    )

    # Tell Django to use our custom manager
    objects = UserManager()

    # Login using email instead of username
    USERNAME_FIELD = "email"

    # No additional fields required during createsuperuser
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email