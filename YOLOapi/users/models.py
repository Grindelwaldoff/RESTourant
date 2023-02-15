from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager


class CustomUserManager(UserManager):
    def create_superuser(self, username, email=None, password=None,
                         **extra_fields):
        extra_fields.setdefault('is_admin', True)
        return super().create_superuser(username, email, password,
                                        **extra_fields)


class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_business = models.BooleanField(default=False)
    is_waiter = models.BooleanField(default=False)

    objects = CustomUserManager()

    picture = models.ImageField(
        verbose_name='Logo',
        upload_to='static/',
        blank=True,
        null=True
    )
    colors = models.CharField(
        max_length=150,
        verbose_name='Цвет приложения:'
    )
    domain = models.CharField(
        blank=True,
        db_index=True,
        max_length=300,
        verbose_name='Доменное имя для бизнеса:',
        help_text='Этот параметр будет использоваться для авторизации'
    )
    owner_email = models.EmailField(
        max_length=254
    )
    owner = models.CharField(
        max_length=150,
        verbose_name='Владелец:',
        help_text='Введите имя владельца.'
    )
    owner_phone = models.CharField(
        blank=True,
        max_length=20
    )


class Waiter(models.Model):
    waiter = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )


class Business(models.Model):
    business = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='business'
    )
