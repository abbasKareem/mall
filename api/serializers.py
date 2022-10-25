from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from .models import *


from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
User = get_user_model()


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'phone',  'first_name',
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
        fields = ['shop_name', 'shop_discription', 'image', 'phone']


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
                   'is_superuser', 'shop_name', 'groups', 'user_permissions']


class AllStateSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['state']


class AllShopsByStateSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['shop_name', 'shop_discription', 'image']
