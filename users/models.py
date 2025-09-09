# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser
    Adds is_admin field to distinguish between admin and normal users
    """
    is_admin = models.BooleanField(default=False, help_text="Designates whether user has admin privileges")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} ({'Admin' if self.is_admin else 'User'})"