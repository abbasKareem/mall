# Generated by Django 4.0.7 on 2022-11-02 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0022_alter_customuser_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='diffrenece',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=15),
        ),
    ]