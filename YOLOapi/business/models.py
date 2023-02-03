from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class Business(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='Business'
    )
    id = models.IntegerField(primary_key=True)
    name = models.CharField(
        max_length=150,
        verbose_name="Название:",
        help_text="Введите название бизнеса.",
        unique=True
    )
    picture = models.ImageField(
        verbose_name='Логотип:',
        upload_to='static/',
        blank=True,
        null=True
    )
    color = models.CharField(
        max_length=150,
        verbose_name='Цвет приложения:'
    )
    domain = models.CharField(
        max_length=300,
        verbose_name='Доменное имя для бизнеса:',
        help_text='Этот параметр будет использоваться для авторизации'
    )
    owner = models.CharField(
        max_length=150,
        verbose_name='Владелец:',
        help_text='Введите имя владельца.'
    )
    owner_email = models.EmailField(
        'Почта владельца.',
        max_length=254,
    )
    owner_phone = PhoneNumberField(
        blank=True
    )


class Waiter(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='waiters'
    )
    name = models.CharField(
        max_length=150,
        verbose_name='Имя официанта:',
        help_text='Введите имя официанта'
    )
    email = models.EmailField(
        max_length=254
    )
