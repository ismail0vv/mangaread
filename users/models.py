from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from users.managers import CustomUserManager
from users.utils import user_avatar_path


class User(AbstractBaseUser, PermissionsMixin):
    """
    A custom user model that extends the base Django user model and
    adds additional fields and methods.
    """

    email = models.CharField(max_length=80, unique=True)
    nickname = models.CharField(max_length=255, unique=True)
    avatar = models.ImageField(upload_to=user_avatar_path, default='avatars/default.jng', blank=True)
    is_active = models.BooleanField(default=True)  # Status of activation
    is_staff = models.BooleanField(default=False)  # Status of admin
    is_superuser = models.BooleanField(default=False) # Status of superuser

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['nickname', 'avatar']

    def __str__(self):
        """Return a string representation of the user."""
        return self.email
