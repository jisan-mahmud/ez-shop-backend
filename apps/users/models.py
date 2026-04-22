# apps/users/models.py
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from users.managers import UserManager


class User(AbstractUser, PermissionsMixin):

    ROLE_CHOICES = (
        ("merchant", "Merchant"),
        ("admin",    "Admin"),
    )

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices= ROLE_CHOICES, blank=True)
    phone = models.CharField(max_length=20, blank=True)

    # attach custom manager
    objects = UserManager()

    USERNAME_FIELD  = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

    @property
    def is_merchant(self):
        return self.role == self.Role.MERCHANT

    @property
    def is_super_admin(self):
        return self.role == self.Role.ADMIN