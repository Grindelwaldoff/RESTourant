from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(max_length=150, blank=False)
    email = models.EmailField(max_length=254, blank=False)

    class Meta:
        ordering = ['username', ]
