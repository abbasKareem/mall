# Generated by Django 4.0.7 on 2022-11-01 20:57

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_alter_customuser_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(default='123456', max_length=20, unique=True, validators=[django.core.validators.RegexValidator(message='Phone number must be 11 digits only.', regex='^\\d{20}')]),
        ),
    ]
