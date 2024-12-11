from django.db import models
from django.contrib.auth.models import AbstractUser


class AdvUser(AbstractUser):
   first_name = models.CharField(max_length=100, blank=True, verbose_name='Имя')
   patronymic = models.CharField(max_length=100, blank=True, verbose_name='Отчество')
   last_name = models.CharField(max_length=100, blank=True, verbose_name='Фамилия')

   class Meta(AbstractUser.Meta):
       pass


class Categories(models.Model):
    name = models.CharField(max_length=200, help_text="Введите название категории")

    def __str__(self):
        return self.name


class Application(models.Model):
    name = models.CharField(max_length=100, blank=True, verbose_name='Название')
    description = models.TextField(max_length=1000, help_text="Описание")
    categories = models.ManyToManyField(Categories, help_text="Выберите категорию")
    photo = models.FileField(upload_to ='uploads/')

    LOAN_STATUS = (
        ('n', 'Новая'),
        ('o', 'Принята в работу'),
        ('d', 'Выполнена'),

    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='n', help_text='Статус заявки')


