from django.db import models
from django.contrib.auth.models import AbstractUser


class AdvUser(AbstractUser):
   first_name = models.CharField(max_length=100, blank=True, verbose_name='Имя')
   patronymic = models.CharField(max_length=100, blank=True, verbose_name='Отчество')
   last_name = models.CharField(max_length=100, blank=True, verbose_name='Фамилия')

   class Meta(AbstractUser.Meta):
       pass


