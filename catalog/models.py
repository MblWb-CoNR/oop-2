from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class AdvUser(AbstractUser):
   first_name = models.CharField(max_length=100, blank=True, verbose_name='Имя')
   patronymic = models.CharField(max_length=100, blank=True, verbose_name='Отчество')
   last_name = models.CharField(max_length=100, blank=True, verbose_name='Фамилия')

   TARIFF_CHOICES = [
       ('company', 'Для юр.лиц'),
       ('individual', 'Для физ.лиц'),
   ]
   tariff = models.CharField(max_length=20, choices=TARIFF_CHOICES, default='individual', verbose_name='Тариф')

   class Meta(AbstractUser.Meta):
       pass


class Categories(models.Model):
    name = models.CharField(max_length=200, help_text="Введите название категории")

    def __str__(self):
        return self.name


class Application(models.Model):
    date = models.DateField(null=True, blank=True)
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(max_length=1000, help_text="Описание")
    categories = models.ManyToManyField(Categories, help_text="Выберите категорию")
    photo = models.FileField(upload_to='photos/')

    LOAN_STATUS = (
        ('n', 'Новая'),
        ('o', 'Принята в работу'),
        ('d', 'Выполнена'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='n', help_text='Статус заявки')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, verbose_name='Пользователь')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена', default=10000, blank=True)
    comment = models.TextField(null=True, blank=True, verbose_name='Комментарий администратора')
    document = models.FileField(upload_to='documents/', null=True, blank=True, verbose_name='Договор')
