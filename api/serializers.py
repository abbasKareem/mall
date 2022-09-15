from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from .models import Product, CustomUser, Order, Category, ProductReview


class UserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['shop_name']


class UserOrderBySerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username']


class RelatedProductSerialzer(ModelSerializer):

    class Meta:
        model = Product
        fields = ['title', 'selling_price', 'image']


class ProductSerializer(ModelSerializer):
    user = UserSerializer()

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


class MyOrderSerializer(ModelSerializer):
    owner = UserSerializer()
    ordered_by = UserOrderBySerializer()

    class Meta:
        model = Order
        depth = 1
        fields = '__all__'


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
        fields = ['shop_name', 'shop_discription', 'image']
