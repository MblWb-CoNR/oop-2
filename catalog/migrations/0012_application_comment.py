# Generated by Django 5.1.4 on 2024-12-13 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0011_application_date_alter_application_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='comment',
            field=models.TextField(blank=True, null=True, verbose_name='Комментарий администратора'),
        ),
    ]
