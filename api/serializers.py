from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from datetime import datetime, timedelta
import random
from django.conf import settings
from .models import *
from .utils import send_otp

from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
User = get_user_model()


class UserSerializerOtp(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, min_length=settings.MIN_PASSWORD_LENGTH, error_messages={
        "min_length": f"Password must be longer than {settings.MIN_PASSWORD_LENGTH} characters"
    })

    password2 = serializers.CharField(
        write_only=True,
        min_length=settings.MIN_PASSWORD_LENGTH,
        error_messages={
            "min_length": f"Password must be longer than {settings.MIN_PASSWORD_LENGTH} characters"}
    )

    class Meta:
        model = CustomUser
        fields = ["id", "phone_number", "email",
                  "username", "password1", "password2"]

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        otp = random.randint(1000, 9999)
        otp_expiry = datetime.now() + timedelta(minutes=10)
        user = CustomUser(
            phone_number=validated_data["phone_number"],
            email=validated_data["email"],
            username=validated_data["username"],
            otp=otp,
            otp_expiry=otp_expiry,
            max_otp_try=settings.MAX_OTP_TRY
        )
        user.set_password(validated_data['password1'])
        user.save()
        is_sent = send_otp(validated_data["phone_number"], otp)
        return user


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'phone_number',  'first_name',
                  'last_name', 'password')


class SizeSerializer(ModelSerializer):
    class Meta:
        model = Size
        exclude = ['id']


class ColorSerializer(ModelSerializer):
    class Meta:
        model = Color
        exclude = ['id']


class UserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'shop_name']


class UserOrderBySerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username']


class RelatedProductSerialzer(ModelSerializer):

    class Meta:
        model = Product
        fields = ['title', 'selling_price', 'image']


class AllProductSerializer(ModelSerializer):
    user = UserSerializer()
    size = SizeSerializer(many=True)
    color = ColorSerializer(many=True)

    class Meta:
        model = Product
        depth = 1
        exclude = ('photo_1', 'photo_2', 'photo_3', 'photo_4', 'photo_5',
                   'photo_6', 'photo_7', 'photo_8', 'photo_9', 'photo_10')

        # fields = '__all__'


class SearchProductSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Product
        fields = ['id', 'title', 'user', 'image', 'selling_price']


class ProductSerializer(ModelSerializer):
    user = UserSerializer()
    size = SizeSerializer(many=True)
    color = ColorSerializer(many=True)

    class Meta:
        model = Product
        depth = 1
        fields = '__all__'


class OrderSerializer(ModelSerializer):
    owner = UserSerializer()
    ordered_by = UserSerializer()

    class Meta:
        model = Order
        depth = 1
        fields = '__all__'


class OrderProductSerializer(ModelSerializer):
    class Meta:
        fields = ['id', 'title']
        model = Product


class ProductMyOrderSerializer(ModelSerializer):
    class Meta:
        model = ProductOrder
        fields = ['title',
                  'selling_price', 'sizes', 'colors', 'quantity_ordered']


class MyOrderSerializer(ModelSerializer):
    owner = UserSerializer()
    # ordered_by = UserOrderBySerializer()
    product = ProductMyOrderSerializer(many=True)

    class Meta:
        model = Order
        depth = 1
        fields = ['id', 'owner', 'product', 'total', 'discount',
                  'total_after_discount', 'order_status', 'created_at']


class CustomUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ('password',)


class RegisterSerializer(ModelSerializer):
    password = serializers.CharField(max_length=6, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductReviewUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username']


class ProductReviewProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id']


class ProductReviewSerializer(serializers.ModelSerializer):
    user = ProductReviewUserSerializer()
    # product = ProductReviewProductSerializer()

    class Meta:
        model = ProductReview
        fields = ['user', 'review_text', 'review_rating']


class ListAllShopSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['shop_name', 'shop_discription', 'image', 'phone_number']


class WishListProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'image', 'selling_price']


class AllWishListSerializer(ModelSerializer):
    products = WishListProductSerializer(many=True)

    class Meta:
        model = WishList
        fields = ['products']


class ShopSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'shop_name', 'image', 'start_date']


class AllFollowersSerializer(ModelSerializer):
    shops = ShopSerializer(many=True)

    class Meta:
        model = Followers
        depth = 1
        fields = ['id', 'shops']


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ['password', 'image', 'last_login', 'shop_discription', 'is_staff',
                   'is_superuser', 'shop_name', 'groups', 'user_permissions', 'otp_expiry', 'otp_max_out', 'max_otp_try', 'state',  'otp']


class AllStateSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['state']


class AllShopsByStateSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['shop_name', 'shop_discription', 'image']
