import random

from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'


class Categories(models.Model):
    """Модель категорий"""

    name = models.CharField(
        max_length=150,
        verbose_name='Наименование:',
        unique=True
    )
    # slug = models.CharField(
    #     'Слаг',
    #     max_length=150,
    #     unique=True,
    #     db_index=True,
    # )
    business = models.ForeignKey(
        User,
        related_name='categories',
        on_delete=models.CASCADE
    )

    def __str__(self):
        """Задаем публичное имя модели"""
        return self.name


class Dishes(models.Model):
    """Модель блюд"""

    name = models.CharField(
        max_length=150,
        verbose_name='Наименование:',
        help_text='Введите название блюда',
        unique=True,
    )
    description = models.CharField(
        max_length=400,
        verbose_name='Описание:',
    )
    composition = models.CharField(
        max_length=400,
        verbose_name='Состав блюда:'
    )
    price = models.FloatField(
        max_length=10,
        verbose_name='Цена блюда:',
        help_text='Введите цену',
    )
    discountPrice = models.FloatField(
        max_length=10,
        verbose_name='Дисконтная цена:',
        help_text='Введите цену'
    )
    currency = models.CharField(
        max_length=150,
        verbose_name='Валюта:'
    )
    picture = models.ImageField(
        verbose_name='Внешний вид блюда:',
        upload_to='static/',
        blank=True,
        null=True
    )
    category = models.ForeignKey(
        Categories,
        null=True,
        on_delete=models.SET_NULL,
        related_name='dishes',
        verbose_name='Категория блюда:',
        help_text='Выберите категорию блюда'
    )
    is_popular = models.BooleanField(
        verbose_name='Востребованность блюда:',
        help_text='☑ - востребованно, ▢ - не востребованно'
    )
    business = models.ForeignKey(
        User,
        related_name='dishes',
        on_delete=models.CASCADE
    )

    def __str__(self):
        """Задаем публичное имя модели"""
        return self.name


class Tables(models.Model):
    """Модель для столов"""

    id = models.IntegerField(
        unique=True,
    )
    hashsalt = models.CharField(
        unique=True,
        primary_key=True,
        editable=False,
        max_length=150
    )
    title = models.CharField(
        max_length=150,
        verbose_name='Описание для стола:',
        null=True,
        blank=True
    )
    business = models.ForeignKey(
        User,
        related_name='tables',
        on_delete=models.CASCADE
    )

    def save(self, *args, **kwargs) -> None:
        self.hashsalt = ''.join(random.choice(alphabet) for i in range(150))
        return super().save(*args, **kwargs)

    def __str__(self):
        return str(self.hashsalt)


class QRCodes(models.Model):
    """Модель для QR-кодов"""

    table = models.ForeignKey(
        Tables,
        on_delete=models.CASCADE,
        related_name='qrcodes',
        verbose_name='Стол:',
        help_text='Выберите стол',
    )
    qrcode = models.CharField(
        max_length=1000000,
        unique=True
    )
    business = models.ForeignKey(
        User,
        related_name='qrcodes',
        on_delete=models.CASCADE
    )
