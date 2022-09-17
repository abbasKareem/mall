# Generated by Django 4.0.7 on 2022-09-17 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_remove_product_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='last_name',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='shop_name',
            field=models.CharField(blank=True, max_length=200, unique=True),
        ),
    ]
