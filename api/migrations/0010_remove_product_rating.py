# Generated by Django 4.0.7 on 2022-09-15 20:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_wishlist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='rating',
        ),
    ]
