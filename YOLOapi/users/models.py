from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):

    def _create_user(self, name, email, password, **extra_fields):
        if not name:
            raise ValueError(('The given name must be set'))
        email = self.normalize_email(email)
        user = self.model(name=name, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, name, email=None, password=None, **extra_fields):
        return self._create_user(name, email, password, False, False, ' ',
                                 **extra_fields)

    def create_superuser(self, name, email, password, **extra_fields):
        user = self._create_user(name, email, password, True, True,
                                 **extra_fields)
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    name = models.CharField(max_length=150, blank=False)
    email = models.EmailField(max_length=254, blank=False)

    class Meta:
        ordering = ['name', ]
