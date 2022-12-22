from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from users.managers import CustomUserManager
from .utils import user_avatar_path


class User(AbstractBaseUser, PermissionsMixin):
    email = models.CharField(max_length=80, unique=True)
    nickname = models.CharField(max_length=255, unique=True)
    avatar = models.ImageField(
        upload_to=user_avatar_path, default='avatars/default.jng', blank=True)
    is_active = models.BooleanField(default=True)  # Статус активации
    is_staff = models.BooleanField(default=False)  # Статус админа
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['nickname', 'avatar']

    def __str__(self):
        return self.email
