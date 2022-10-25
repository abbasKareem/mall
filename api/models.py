from django.db import models
from django.utils.html import mark_safe
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.conf import settings
from decimal import Decimal

from colorfield.fields import ColorField

from django.db.models.signals import post_save
from django.dispatch import receiver

from django_admin_geomap import GeoItem


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, phone, username, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        # other_fields.setdefault('is_active', True)

        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, phone, username, password, **other_fields)

    def create_user(self, email, phone, username, password, **other_fields):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)

        if not phone:
            raise ValueError('You must provide phone number')

        user = self.model(email=email, phone=phone,
                          username=username, **other_fields)
        user.set_password(password)
        user.save()
        return user


STATES = (
    ("بغداد", "بغداد"),
    ("الانبار", "الانبار"),
    ("بابل", "بابل"),
    ("بصرة", "بصرة"),
    ("ذي قار", "ذي قار"),
    ("ديالى", "ديالى"),
    ("دهوك", "دهوك"),
    ("اربيل", "اربيل"),
    ("كربلاء", "كربلاء"),
    ("كركوك", "كركوك"),
    ("ميسان", "ميسان"),
    ("المثنى", "المثنى"),
    ("النجف", "النجف"),
    ("الموصل", "الموصل"),
    ("صلاح الدين", "صلاح الدين"),
    ("سليمانية", "سليمانية"),
    ("واسط", "واسط"),
)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        max_length=100, unique=True, default='test@gmail.com')
    phone = models.CharField(max_length=20, unique=True, default='07801234567')
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    start_date = models.DateTimeField(default=timezone.now)
    image = models.ImageField(
        upload_to="users/%Y/%m/%d/", blank=True, null=True)
    shop_discription = models.TextField(blank=True, null=True)
    state = models.CharField(max_length=20, null=True,
                             blank=True, choices=STATES, default=STATES[0])

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    shop_name = models.CharField(
        max_length=200, blank=True, unique=True, null=True)
    points = models.IntegerField(default=0)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone', 'username',  'first_name', 'last_name']

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'المستخدم'
        verbose_name_plural = 'المستخدمين'


class Category(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'الصنف'
        verbose_name_plural = 'الاصناف'


SIZES = (
    ("S", "S"),
    ("M", "M"),
    ("L", "L"),
    ("XL", "XL"),
    ("XXL", "XXL"),
)


class Size(models.Model):
    size_name = models.CharField(max_length=4)

    def __str__(self):
        return self.size_name

    class Meta:
        verbose_name = 'الحجم'
        verbose_name_plural = 'الاحجام'


class Color(models.Model):
    color_name = models.CharField(max_length=20, blank=True, unique=True)
    color_code = ColorField(default='#FF0000')

    def __str__(self):
        return self.color_name

    class Meta:
        verbose_name = 'اللون'
        verbose_name_plural = 'الالوان'

    def the_color(self):
        string_my = f"<div style='width: 30px; height: 30px; background-color: {self.color_code};border-radius: 50%;'></div>"
        return mark_safe(string_my)


class Product(models.Model):
    class ProductObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(is_public=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    size = models.ManyToManyField(Size)
    color = models.ManyToManyField(Color, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    image = models.ImageField(upload_to="products/%Y/%m/%d/", blank=False)
    price = models.DecimalField(max_digits=15, decimal_places=2, default=99.99)
    selling_price = models.DecimalField(
        max_digits=15, decimal_places=2, default=99.99, blank=False)
    description = models.TextField()
    warranty = models.CharField(max_length=300, null=True, blank=True)
    return_policy = models.CharField(max_length=300, null=True, blank=True)
    view_count = models.PositiveIntegerField(default=0)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    photo_1 = models.ImageField(upload_to='products/%Y/%m/%d/', blank=True)
    photo_2 = models.ImageField(upload_to='products/%Y/%m/%d/', blank=True)
    photo_3 = models.ImageField(upload_to='products/%Y/%m/%d/', blank=True)
    photo_4 = models.ImageField(upload_to='products/%Y/%m/%d/', blank=True)
    photo_5 = models.ImageField(upload_to='products/%Y/%m/%d/', blank=True)
    photo_6 = models.ImageField(upload_to='products/%Y/%m/%d/', blank=True)
    photo_7 = models.ImageField(upload_to='products/%Y/%m/%d/', blank=True)
    photo_8 = models.ImageField(upload_to='products/%Y/%m/%d/', blank=True)
    photo_9 = models.ImageField(upload_to='products/%Y/%m/%d/', blank=True)
    photo_10 = models.ImageField(upload_to='products/%Y/%m/%d/', blank=True)

    objects = models.Manager()
    productobjects = ProductObjects()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'المنتج'
        verbose_name_plural = 'المنتجات'

    def the_image(self):
        return mark_safe('<img src="%s" width="100" />' % (self.image.url))

    def save(self, *args, **kwargs):
        if self.quantity <= 0:
            self.is_public = False
        super(Product, self).save(*args, **kwargs)


# class Cart(models.Model):
#     # Customer may have many carts, but cart only belong to one customer
#     customer = models.ForeignKey(
#         settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
#     total = models.PositiveIntegerField(default=0)
#     created_at = models.DateTimeField(auto_now_add=True)
#     shop = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='the_shop',
#                              on_delete=models.SET_NULL, null=True, blank=True)

#     def __str__(self):
#         return "Cart: " + str(self.id)


# class CartProduct(models.Model):
#     # a Cart may have many CartProduct,
#     cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     rate = models.PositiveIntegerField()
#     quantity = models.PositiveIntegerField()
#     subtotal = models.PositiveIntegerField()

#     def __str__(self):
#         return "Cart: " + str(self.cart.id) + " CartProduct: " + str(self.id)


# class ProductItems(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField()
#     colors = models.ManyToManyField(Color,  blank=True)
#     sizes = models.ManyToManyField(Size,  blank=True)

#     def __str__(self):
#         return f"{self.product.title},  quantity: {self.quantity}"


ORDER_STATUS = (
    ("Order Received", "Order Recevied"),
    ("Order Processing", "Order Processing"),
    ("on the way", "on the way"),
    ("Order Complated", "Order Complated"),
    ("Order Canceled", "Order Canceled")
)

DISCOUNT_STATUS = (
    ("No Discound", "No Discound"),
    ("5 % Discount", "5 % Discount"),
    ("10 % Discount", "10 % Discount"),
    ("20 % Discount", "20 % Discount"),
    ("30 % Discount", "30 % Discount"),
    ("40 % Discount", "40 % Discount"),
    ("50 % Discount", "50 % Discount"),
)


# ===========================================================================================
class ProductOrder(models.Model):
    shop = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=200)
    sizes = models.CharField(max_length=200, null=True, blank=True)
    colors = models.CharField(max_length=200, null=True, blank=True)
    quantity_ordered = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=15, decimal_places=2, default=99.99)
    selling_price = models.DecimalField(
        max_digits=15, decimal_places=2, default=99.99, blank=False)

    def __str__(self):
        return self.title
# ===========================================================================================


class Order(models.Model, GeoItem):
    # cart = models.OneToOneField(
    #     Cart, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ManyToManyField(ProductOrder, null=True, blank=True)
    ordered_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='the_owner', default=1)
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
    created_at = models.DateTimeField(default=timezone.now)
    lon = models.FloatField(default=33.4978)  # longitude
    lat = models.FloatField(default=33.4978)  # latitude
    message = models.TextField(blank=True, null=True)

    @property
    def geomap_longitude(self):
        return '' if self.lon is None else str(self.lon)

    @property
    def geomap_latitude(self):
        return '' if self.lon is None else str(self.lat)

    def __str__(self):
        return "Order: " + str(self.id) + " - "+"Customer: " + str(self.ordered_by) + "  - " + "Date: " + str(self.created_at.date())
        # return str(self.created_at)

    class Meta:
        verbose_name = 'الطلب'
        verbose_name_plural = 'الطلبات'

    def save(self, *args, **kwargs):
        if self.total:
            self.total_after_discount = self.total
            if self.discount == "No Discound":
                self.total_after_discount = self.total
            if self.discount == "5 % Discount":
                self.total_after_discount = self.total - \
                    (self.total * Decimal(0.05))
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
        return f"( {self.user.username} ) user comment on product:  ( {self.product.title} )"


class WishList(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)

    def __str__(self):
        return f"{self.user.username}"


class Followers(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    shops = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='shops')

    def __str__(self):
        return f"{self.user.username} follow {self.shops}"


class Complaint(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"User {self.user.username} complaint {self.id}"

    class Meta:
        verbose_name = 'الشكوى'
        verbose_name_plural = 'الشكاوي'
