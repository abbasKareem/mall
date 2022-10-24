from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.decorators import (api_view, permission_classes,
                                       renderer_classes)
from django.shortcuts import render
from django.http import HttpResponseRedirect
# from django.contrib.sites.models import Site
from django.contrib import messages
import requests
from rest_framework.parsers import BaseParser
import re
import base64
import pprint
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination, BasePagination

import django_filters.rest_framework
from rest_framework import generics
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import authentication
from rest_framework import pagination

from .models import *
# from .serializers import ProductSerializer, CustomUserSerializer, OrderSerializer, MyOrderSerializer, RegisterSerializer, CategorySerializer, ProductReviewSerializer
from .serializers import *

from django.contrib.auth.hashers import make_password

# =================Products============


class ListProductView(generics.ListCreateAPIView):
    queryset = Product.productobjects.all().order_by('-id')
    serializer_class = AllProductSerializer
    # pagination_class = PageNumberPagination
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        title = request.data.get('title')
        paginator = LimitOffsetPagination()
        if title is None or "":
            products = Product.productobjects.all().order_by('-id')[:20]
            result_page = paginator.paginate_queryset(products, request)
            serializer = SearchProductSerializer(result_page, many=True)
            return Response(serializer.data)
            # return paginator.get_paginated_response(serializer.data)
            # return self.get_paginated_response(serializer.data)

        products = Product.productobjects.filter(title__icontains=title)[:20]
        serializer = SearchProductSerializer(products, many=True)
        return Response(serializer.data)
        # return self.get_paginated_response(data=serializer.data)


class SearchProductView(APIView, LimitOffsetPagination):
    product_serializer = AllProductSerializer

    def get(self, request, query):
        products = Product.productobjects.filter(title__icontains=query)
        result = self.paginate_queryset(products, request)
        serializer = self.product_serializer(result, many=True)
        return self.get_paginated_response(serializer.data)


class ListProductByShopName(APIView, LimitOffsetPagination):
    queryset = Product.productobjects.all()
    serializer_class = AllProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, name=None):

        shop_exist = CustomUser.objects.filter(shop_name=name).first()
        if shop_exist:
            products = Product.productobjects.filter(
                user__shop_name=name).order_by('-id')
            result = self.paginate_queryset(products, request)
            serializer = self.serializer_class(result, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            return Response({'message': 'Shop Not Found'}, status=status.HTTP_404_NOT_FOUND)


class ListProductByViewCountName(generics.ListAPIView):
    queryset = Product.productobjects.all().order_by('-view_count', 'id')
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class DetailProductView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ProductSerializer

    def get(self, request, pk=None):
        try:
            product = Product.productobjects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({'message': 'Product not found with this id'}, status=status.HTTP_404_NOT_FOUND)
        shop_name = product.user
        print(shop_name.pk)

        related_products = Product.productobjects.filter(
            category=product.category, user=shop_name.pk).exclude(pk=pk)[:4]

        # print(related_products.first().title)
        related_products_serializer = RelatedProductSerialzer(
            related_products, many=True)

        product.view_count += 1
        product.save()
        serializer = ProductSerializer(product)

        product_reviews = ProductReview.objects.filter(product=product)
        product_reviews_serializer = ProductReviewSerializer(
            product_reviews, many=True)

        prdoucts_dict = {
            'product': serializer.data,
            'related_products': related_products_serializer.data,
            'product_reviews': product_reviews_serializer.data
        }
        return Response(prdoucts_dict)


class ListProductReviewView(generics.ListAPIView):
    queryset = ProductReview.objects.all()
    serializer_class = ProductSerializer


class LowProductView(generics.ListAPIView):
    queryset = Product.productobjects.all().order_by('price')
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ProductSerializer


class HighProductView(generics.ListAPIView):
    queryset = Product.productobjects.all().order_by('-price')
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ProductSerializer


class ProductReviewView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk=None):
        # try:
        review_text = request.data.get('review_text')
        review_rating = request.data.get('review_rating')

        review_check = ProductReview.objects.filter(
            user=request.user.pk, product=pk).count()
        if review_check > 0:
            return Response({'message': 'You already rating this product!'}, status=status.HTTP_400_BAD_REQUEST)

        user = CustomUser.objects.get(id=request.user.pk)
        print(request.user.pk)

        try:
            product = Product.objects.get(id=pk)
        except Product.DoesNotExist:
            return Response({'message': 'Product with this id does not exist!'}, status=status.HTTP_404_NOT_FOUND)

        review_created = ProductReview.objects.create(
            user=request.user, product=product, review_rating=review_rating, review_text=review_text)
        review_created.save()

        return Response({'review_text': review_created.review_text, 'review_rating': review_created.review_rating}, status=status.HTTP_201_CREATED)


# =================Products============

# =================Categories============


class ListCategoryView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ListProductsByCategoryIdView(APIView, LimitOffsetPagination):
    queryset = Category.objects.all()
    serializer_class = AllProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, pk=None):
        products = Product.productobjects.filter(category=pk).order_by('-id')
        if products:
            result = self.paginate_queryset(products, request)
            serializer = self.serializer_class(result, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            return Response({'message': 'Not valid category id'})


# =================Categories============


# =================Orders============
class ListMyOrderView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = MyOrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        user = request.user
        order_query_set = Order.objects.filter(ordered_by=user).order_by('-id')
        if order_query_set.count() == 0:
            return Response({'message': "You don't have order yet"})
        serializer = MyOrderSerializer(order_query_set, many=True)
        return Response(serializer.data)


class DetailOrderView(generics.RetrieveAPIView):
    serializer_class = MyOrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk=None):
        user = request.user
        user_query_set = CustomUser.objects.filter(username=user).first()
        order_query_set = Order.objects.filter(ordered_by=user_query_set.pk)
        order_query_set = get_object_or_404(order_query_set, pk=pk)

        serializer = MyOrderSerializer(order_query_set)
        return Response(serializer.data)


class OrderCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        ordered_by = request.user
        user = CustomUser.objects.get(username=request.user)
        shop_name = request.data.get('shop_name')
        lon = request.data.get('lon')
        lat = request.data.get('lat')
        message = request.data.get('message')
        products = request.data.get('products')
        total = request.data.get('total')

        try:
            shop_obj = CustomUser.objects.get(shop_name=shop_name)

            PRODUCTS_OBJECTS = []
            QUANTITY = []
            PRODUCTS_IDS = []
            COLORS = []
            SIZES = []

            for p in products:
                for key, value in p.items():
                    if key == 'id':
                        PRODUCTS_IDS.append(value)
                    if key == 'quantity':
                        QUANTITY.append(value)
                    if key == 'sizes':
                        SIZES.append(value)
                    if key == 'colors':
                        COLORS.append(value)
            counter = 0

            total_test = 0

            for value in PRODUCTS_IDS:
                try:
                    product_obj = Product.objects.get(id=value)
                except Product.DoesNotExist:
                    return Response({'message': f"Erorr: Product of id number {value} not found"}, status=status.HTTP_404_NOT_FOUND)
                if product_obj.user.shop_name != shop_obj.shop_name:
                    error_messsage = f"Error: The [{product_obj.title}] Does not belong to this shop, try again"
                    return Response({'message': error_messsage}, status=status.HTTP_404_NOT_FOUND)
                # total_test += product_obj.selling_price
                product_order_obj = ProductOrder.objects.create(
                    shop=shop_obj, title=product_obj.title, sizes=SIZES[counter], colors=COLORS[counter], price=product_obj.price, selling_price=product_obj.selling_price, quantity_ordered=QUANTITY[counter])
                product_order_obj.save()
                total_test += product_obj.selling_price * QUANTITY[counter]
                counter += 1
                PRODUCTS_OBJECTS.append(product_order_obj)
            order = Order.objects.create(ordered_by=ordered_by, owner=shop_obj, email=request.user.email, mobile=request.user.phone,
                                         total=total_test, order_status='Order Recevied', lat=lat, lon=lon, message=message, discount='No Discound')
            order.save_base()
            for p in PRODUCTS_OBJECTS:
                order.product.add(p)

            order.save()

            qua = 0
            for q in QUANTITY:
                qua += q
            print(total_test)

            user.points += qua * 10
            user.save()

            return Response({'message': 'Order Created Successfully'}, status=status.HTTP_201_CREATED)
        except CustomUser.DoesNotExist:
            return Response({'message': "Error: No shop found with this name"}, status=status.HTTP_404_NOT_FOUND)

# =================Orders============


class RegisterAPIView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# =================Shops============
class ListAllShopView(generics.ListAPIView):
    queryset = CustomUser.objects.filter(is_staff=True).exclude(shop_name__isnull=True).only(
        'username', 'shop_discription', 'image', 'phone')
    serializer_class = ListAllShopSerializer

# =================Shops============


# =================WishList============
class WishListCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        product = request.data.get('product')
        user = CustomUser.objects.get(username=request.user)
        if WishList.objects.filter(products=product, user=user).exists():
            return Response({'message': 'Product already add to you wishlist!'}, status=status.HTTP_200_OK)

        try:
            wish_list = WishList.objects.get(user__username=request.user)
            wish_list.products.add(product)
            wish_list.save()

        except WishList.DoesNotExist:
            wish_list = WishList.objects.create(user=user)
            wish_list.save()
            wish_list.products.add(product)
            wish_list.save()

        print(request.user)
        return Response({'message': 'Product added to your wishlist Successfully!'}, status=status.HTTP_201_CREATED)


class AllWishListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        all_wish_list = WishList.objects.filter(
            user__username=request.user).order_by('-id')[:30]
        if not all_wish_list:
            return Response({'message': "You don't have any wishlist yet"}, status=status.HTTP_200_OK)

        serializer = AllWishListSerializer(all_wish_list, many=True)

        return Response(serializer.data)


class DeleteWishListView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, id=None):
        try:
            if not Product.objects.filter(pk=id).exists():
                return Response({'message': "No product found with this id"}, status=status.HTTP_404_NOT_FOUND)

            wish_list = WishList.objects.get(user__username=request.user)

            product = Product.objects.get(pk=id)
            wish_list.products.remove(product)
            wish_list.save()
        except WishList.DoesNotExist:
            return Response({'message': "No wish list found with this id"}, status=status.HTTP_404_NOT_FOUND)
        return Response({'message', 'wish list deleted successfully'}, status=status.HTTP_200_OK)


# =================WishList============


# =================Followers============


class FollowersCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        shop_name = request.data.get('shop_name')
        user = CustomUser.objects.get(username=request.user)

        try:
            try:
                shop_obj = CustomUser.objects.get(shop_name=shop_name)
            except CustomUser.DoesNotExist:
                return Response({'message': 'No Shop found with this name'}, status=status.HTTP_404_NOT_FOUND)

            try:
                already_follow = Followers.objects.get(
                    user=user, shops=shop_obj)
                return Response({'message': 'You already follow this shop'}, status=status.HTTP_200_OK)
            except:
                follow = Followers.objects.get(user__username=request.user)
                follow.shops.add(shop_obj)
                follow.save()

        except Followers.DoesNotExist:
            follow = Followers.objects.create(user=user)
            follow.save()
            follow.shops.add(shop_obj)
            follow.save()

        return Response({'message': 'You successfully follow this shop'}, status=status.HTTP_201_CREATED)


class AllFollowersView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        all_follower = Followers.objects.filter(
            user__username=request.user).order_by('-id')
        if not all_follower:
            return Response({'message': "You are not following any shop"}, status=status.HTTP_200_OK)

        serializer = AllFollowersSerializer(all_follower, many=True)

        return Response(serializer.data)


class UnfollowView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, shop_name=None):
        try:
            if not CustomUser.objects.filter(shop_name=shop_name).exists():
                return Response({'message': "Shop not exist, Please provide valid shop name"}, status=status.HTTP_404_NOT_FOUND)

            all_follower = Followers.objects.get(user__username=request.user)

            shop = CustomUser.objects.get(shop_name=shop_name)
            all_follower.shops.remove(shop)
            all_follower.save()
        except Followers.DoesNotExist:
            return Response({'message': "No follower list found with this name"}, status=status.HTTP_404_NOT_FOUND)
        return Response({'message': 'Unfollow shop successfully'}, status=status.HTTP_200_OK)


# =================Followers============


class OrderCreateTestView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        ordered_by = request.user
        shop_name = request.data.get('shop_name')
        mobile = request.data.get('mobile')
        lon = request.data.get('lon')
        lat = request.data.get('lat')
        message = request.data.get('message')
        products = request.data.get('product')

        my_list = []
        my_quantity = []
        my_colors = []
        for p in products:
            for key, value in p.items():
                if key == 'id':
                    pro_obj = Product.objects.get(pk=value)
                    my_list.append(pro_obj)

        for p in products:
            for key, value in p.items():
                if key == 'quantity':
                    my_quantity.append(value)

        for p in products:
            for key, value in p.items():
                if key == 'colors':
                    my_colors.append(value)
                    print(value)

        return Response({'message': products}, status=status.HTTP_201_CREATED)


class ProfileView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        try:
            user_obj = CustomUser.objects.get(username=request.user)
        except CustomUser.DoesNotExist:
            return Response({'message': 'User not exist!'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProfileSerializer(user_obj)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ChangePasswordView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if not request.data['password']:
            return Response({'message': 'Please provide new Password'}, status=status.HTTP_400_BAD_REQUEST)

        if not re.fullmatch(r'[A-Za-z0-9@#$%^&+=]{8,}', request.data.get('password')):
            return Response({'message': 'Please provide strong password'}, status=status.HTTP_400_BAD_REQUEST)

        password = request.data['password']

        user_obj = CustomUser.objects.filter(username=request.user).first()
        user_obj.password = make_password(password)
        user_obj.save()
        return Response({'message': 'Password updated Successfully'}, status=status.HTTP_200_OK)


def user_activate_account(request, uid, token):
    context = {
        'uid': uid,
        'token': token
    }
    return render(request, 'user_activate_account.html', context=context)


def user_activate_account_succcess(request):
    return render(request, 'user_activate_account_succcess.html')


def reset_user_password(request, uid, token):
    context = {
        'uid': uid,
        'token': token
    }
    return render(request, 'reset_user_password.html', context=context)


def reset_password_success(request):
    return render(request, 'password_done.html')


class AddToCartView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # get prdouct id from requested url
        product_id = request.data.get('pro_id')

        #  then get product
        product_obj = Product.objects.get(id=product_id)

        # check if cart exists
        cart_id = Cart.objects.filter(customer=request.user).last()

        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id.pk)
            this_product_in_cart = cart_obj.cartproduct_set.filter(
                product=product_obj)

        #     # item already exists in cart
            if this_product_in_cart.exists():
                cartproduct = this_product_in_cart.last()
                cartproduct.quantity += 1
                cartproduct.subtotal += product_obj.selling_price
                cartproduct.save()
                cart_obj.total += product_obj.selling_price
                cart_obj.save()

        #     # new item is added in cart
            else:
                cartproduct = CartProduct.objects.create(cart=cart_obj,
                                                         product=product_obj,
                                                         rate=product_obj.selling_price,
                                                         quantity=1,
                                                         subtotal=product_obj.selling_price
                                                         )
                cart_obj.total += product_obj.selling_price
                cart_obj.save()

        # If cart does not exist in the database
        else:
            cart_obj = Cart.objects.create(total=0, customer=request.user)
            # self.request.session['cart_id'] = cart_obj.id

            cartproduct = CartProduct.objects.create(cart=cart_obj,
                                                     product=product_obj,
                                                     rate=product_obj.selling_price,
                                                     quantity=1,
                                                     subtotal=product_obj.selling_price
                                                     )
            cart_obj.total += product_obj.selling_price
            cart_obj.save()

        return Response({'message': 'product added to cart successfully'}, status=status.HTTP_201_CREATED)


class ComplaintCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        user = request.user
        text = request.data.get('text', '')

        Complaint.objects.create(user=user, text=text).save()
        return Response({'message': 'your complaint created successfully'}, status=status.HTTP_201_CREATED)


def index(request):
    return render(request, 'homepage.html')
