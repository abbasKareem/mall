from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.conf import settings
from decimal import Decimal

from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, username, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        # other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, username, password, **other_fields)

    def create_user(self, email, username, password, **other_fields):

        if not email:
            raise ValueError('You must provide an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **other_fields)
        user.set_password(password)
        user.save()
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    image = models.ImageField(
        upload_to="users/%Y/%m/%d/", blank=True, null=True)
    shop_discription = models.TextField(blank=True, null=True)

    is_staff = models.BooleanField(default=False)
    # is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    shop_name = models.CharField(max_length=200, blank=True)
    points = models.IntegerField(default=0)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'المستخدمين'
        verbose_name_plural = 'المستخدمين'


class Category(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'الاصناف'
        verbose_name_plural = 'الاصناف'


class Product(models.Model):
    class ProductObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(is_public=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to="products/%Y/%m/%d/", blank=False)
    price = models.DecimalField(max_digits=15, decimal_places=2, default=99.99)
    selling_price = models.DecimalField(
        max_digits=15, decimal_places=2, default=99.99, blank=False)
    description = models.TextField()
    warranty = models.CharField(max_length=300, null=True, blank=True)
    return_policy = models.CharField(max_length=300, null=True, blank=True)
    view_count = models.PositiveIntegerField(default=0)
    is_public = models.BooleanField(default=True)
    objects = models.Manager()
    productobjects = ProductObjects()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'المنتجات'
        verbose_name_plural = 'المنتجات'


ORDER_STATUS = (
    ("Order Received", "Order Recevied"),
    ("Order Processing", "Order Processing"),
    ("on the way", "on the way"),
    ("Order Complated", "Order Complated"),
    ("Order Canceled", "Order Canceled")
)

DISCOUNT_STATUS = (
    ("No Discound", "No Discound"),
    ("10 % Discount", "10 % Discount"),
    ("20 % Discount", "20 % Discount"),
    ("30 % Discount", "30 % Discount"),
    ("40 % Discount", "40 % Discount"),
    ("50 % Discount", "50 % Discount"),
)


class Order(models.Model):
    # cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product)
    ordered_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='the_owner', default=1)
    shipping_address = models.CharField(max_length=200)
    mobile = models.CharField(max_length=15)
    email = models.EmailField(null=True, blank=True)
    total = models.DecimalField(
        max_digits=15, decimal_places=2, blank=True, null=True)
    discount = models.CharField(
        max_length=50, choices=DISCOUNT_STATUS, default=DISCOUNT_STATUS[0])
    total_after_discount = models.DecimalField(
        max_digits=15, decimal_places=2, default=0)
    order_status = models.CharField(
        max_length=50, choices=ORDER_STATUS, default=ORDER_STATUS[0])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Order: " + str(self.id)

    class Meta:
        verbose_name = 'الطلبات'
        verbose_name_plural = 'الطلبات'

    def save(self, *args, **kwargs):
        if self.total:
            self.total_after_discount = self.total
            if self.discount == "No Discound":
                self.total_after_discount = self.total
            if self.discount == "10 % Discount":
                self.total_after_discount = self.total - \
                    (self.total * Decimal(0.1))
            if self.discount == "20 % Discount":
                self.total_after_discount = self.total - \
                    (self.total * Decimal(0.2))
            if self.discount == "30 % Discount":
                self.total_after_discount = self.total - \
                    (self.total * Decimal(0.3))
            if self.discount == "40 % Discount":
                self.total_after_discount = self.total - \
                    (self.total * Decimal(0.4))
            if self.discount == "50 % Discount":
                self.total_after_discount = self.total - \
                    (self.total * Decimal(0.5))

            return super(Order, self).save(*args, **kwargs)


RATING = (
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
)


class ProductReview(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review_text = models.TextField()
    review_rating = models.IntegerField(choices=RATING, default=RATING[0])

    class Meta:
        verbose_name = 'التعليقات و التقيمات'
        verbose_name_plural = 'التعليقات و التقيمات'

    def __str__(self):
        # return str(self.user.username) + " \t  Coment on Product:   " + str(self.product.title)
        return f"( {self.user.username} ) user comment on product:  ( {self.product.title} )"


class WishList(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)

    def __str__(self):
        return f"{self.user.username}"
