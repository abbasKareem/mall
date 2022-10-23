# Generated by Django 4.0.7 on 2022-10-04 17:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_admin_geomap


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('phone', models.CharField(default='07801234567', max_length=20, unique=True)),
                ('username', models.CharField(max_length=150, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=50, null=True)),
                ('last_name', models.CharField(blank=True, max_length=50, null=True)),
                ('start_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('image', models.ImageField(blank=True, null=True, upload_to='users/%Y/%m/%d/')),
                ('shop_discription', models.TextField(blank=True, null=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('shop_name', models.CharField(blank=True, max_length=200, null=True, unique=True)),
                ('points', models.IntegerField(default=0)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'المستخدم',
                'verbose_name_plural': 'المستخدمين',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'الصنف',
                'verbose_name_plural': 'الاصناف',
            },
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color_name', models.CharField(blank=True, max_length=20, unique=True)),
                ('color_code', models.CharField(blank=True, max_length=20, null=True)),
            ],
            options={
                'verbose_name': 'اللون',
                'verbose_name_plural': 'الالوان',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('quantity', models.IntegerField(default=1)),
                ('image', models.ImageField(upload_to='products/%Y/%m/%d/')),
                ('price', models.DecimalField(decimal_places=2, default=99.99, max_digits=15)),
                ('selling_price', models.DecimalField(decimal_places=2, default=99.99, max_digits=15)),
                ('description', models.TextField()),
                ('warranty', models.CharField(blank=True, max_length=300, null=True)),
                ('return_policy', models.CharField(blank=True, max_length=300, null=True)),
                ('view_count', models.PositiveIntegerField(default=0)),
                ('is_public', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('photo_1', models.ImageField(blank=True, upload_to='products/%Y/%m/%d/')),
                ('photo_2', models.ImageField(blank=True, upload_to='products/%Y/%m/%d/')),
                ('photo_3', models.ImageField(blank=True, upload_to='products/%Y/%m/%d/')),
                ('photo_4', models.ImageField(blank=True, upload_to='products/%Y/%m/%d/')),
                ('photo_5', models.ImageField(blank=True, upload_to='products/%Y/%m/%d/')),
                ('photo_6', models.ImageField(blank=True, upload_to='products/%Y/%m/%d/')),
                ('photo_7', models.ImageField(blank=True, upload_to='products/%Y/%m/%d/')),
                ('photo_8', models.ImageField(blank=True, upload_to='products/%Y/%m/%d/')),
                ('photo_9', models.ImageField(blank=True, upload_to='products/%Y/%m/%d/')),
                ('photo_10', models.ImageField(blank=True, upload_to='products/%Y/%m/%d/')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.category')),
                ('color', models.ManyToManyField(to='api.color')),
            ],
            options={
                'verbose_name': 'المنتج',
                'verbose_name_plural': 'المنتجات',
            },
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size_name', models.CharField(choices=[('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL'), ('XXL', 'XXL')], default=('S', 'S'), max_length=4)),
            ],
            options={
                'verbose_name': 'الحجم',
                'verbose_name_plural': 'الاحجام',
            },
        ),
        migrations.CreateModel(
            name='WishList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('products', models.ManyToManyField(to='api.product')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProductReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_text', models.TextField()),
                ('review_rating', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], default=(1, '1'))),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'التعليقات و التقيمات',
                'verbose_name_plural': 'التعليقات و التقيمات',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='size',
            field=models.ManyToManyField(to='api.size'),
        ),
        migrations.AddField(
            model_name='product',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.CharField(max_length=15)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('total', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('discount', models.CharField(choices=[('No Discound', 'No Discound'), ('5 % Discount', '5 % Discount'), ('10 % Discount', '10 % Discount'), ('20 % Discount', '20 % Discount'), ('30 % Discount', '30 % Discount'), ('40 % Discount', '40 % Discount'), ('50 % Discount', '50 % Discount')], default=('No Discound', 'No Discound'), max_length=50)),
                ('total_after_discount', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
                ('order_status', models.CharField(choices=[('Order Received', 'Order Recevied'), ('Order Processing', 'Order Processing'), ('on the way', 'on the way'), ('Order Complated', 'Order Complated'), ('Order Canceled', 'Order Canceled')], default=('Order Received', 'Order Recevied'), max_length=50)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('lon', models.FloatField(default=33.4978)),
                ('lat', models.FloatField(default=33.4978)),
                ('message', models.TextField(blank=True, null=True)),
                ('ordered_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='the_owner', to=settings.AUTH_USER_MODEL)),
                ('product', models.ManyToManyField(to='api.product')),
            ],
            options={
                'verbose_name': 'الطلب',
                'verbose_name_plural': 'الطلبات',
            },
            bases=(models.Model, django_admin_geomap.GeoItem),
        ),
        migrations.CreateModel(
            name='Followers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shops', models.ManyToManyField(related_name='shops', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
