from django.db import models
from django.contrib.auth.models import AbstractUser


class AdvUser(AbstractUser):
   first_name = models.CharField(max_length=100, blank=True, verbose_name='Имя')
   patronymic = models.CharField(max_length=100, blank=True, verbose_name='Отчество')
   last_name = models.CharField(max_length=100, blank=True, verbose_name='Фамилия')

   class Meta(AbstractUser.Meta):
       pass


class Tarif(models.Model):
    name = models.CharField(max_length=100, blank=True, verbose_name='Тариф')

    def __str__(self):
        return self.name