from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg

import django_filters.rest_framework
from rest_framework import generics
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import authentication
from rest_framework import pagination

from .models import Product,  CustomUser, Order, Category, ProductReview
# from .serializers import ProductSerializer, CustomUserSerializer, OrderSerializer, MyOrderSerializer, RegisterSerializer, CategorySerializer, ProductReviewSerializer
from .serializers import *

# =================Products============


class ListProductView(generics.ListCreateAPIView):
    queryset = Product.productobjects.all().order_by('-id')
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        title = request.data.get('title')
        if title is None:
            products = Product.productobjects.all().order_by('-id')
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)

        products = Product.productobjects.filter(title__icontains=title)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ListProductByShopName(generics.ListAPIView):
    queryset = Product.productobjects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def list(self, request, name=None):
        shop_exist = CustomUser.objects.filter(shop_name=name).first()
        if shop_exist:
            products = Product.productobjects.filter(
                user__shop_name=name).order_by('-id')
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)
            # self.get_paginated_response(serializer.data)
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
        product = Product.productobjects.get(pk=pk)
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


class ListProductsByCategoryIdView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def list(self, request, pk=None):
        products = Product.productobjects.filter(category=pk)
        if products:
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)
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
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        ordered_by = request.user
        user = CustomUser.objects.get(username=request.user)
        shop_name = request.data.get('shop_name')
        shipping_address = request.data.get('shipping_address')
        mobile = request.data.get('mobile')
        product = request.data.get('product')
        # print(product)
        PRODUCTS_IDS = []
        PRODUCTS_OBJECTS = []

        for p in product:
            PRODUCTS_IDS.append(p)

        total = 0
        for p in PRODUCTS_IDS:
            # try:
            my_product = Product.objects.get(id=p)
            # print(my_product.title)
            PRODUCTS_OBJECTS.append(my_product)
            # except Product.DoesNotExist:
            #     return Response({'message': 'No product found with this id'}, status=status.HTTP_404_NOT_FOUND)

            total += my_product.selling_price
        try:
            owner = CustomUser.objects.get(shop_name=shop_name)
        except CustomUser.DoesNotExist:
            return Response({"message": "No shop name found"}, status=status.HTTP_404_NOT_FOUND)

        order = Order.objects.create(ordered_by=ordered_by, owner=owner, email=user.email, mobile=mobile,
                                     total=total, shipping_address=shipping_address, order_status='Order Recevied')
        order.save()
        for p in PRODUCTS_OBJECTS:
            order.product.add(p)
            # order.save()
            # print(p.title)
        order.save()

        user.points += 10
        user.save()

        return Response({'message': 'Order Created Successfully'}, status=status.HTTP_201_CREATED)
# =================Orders============


class RegisterAPIView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListAllShopView(generics.ListAPIView):
    queryset = CustomUser.objects.filter(is_staff=True).only(
        'username', 'shop_discription', 'image')
    serializer_class = ListAllShopSerializer
    # def list(self, request):
    #     pass

    # def create(self, request):
    #     pass

    # def retrieve(self, request, pk=None):
    #     pass

    # def update(self, request, pk=None):
    #     pass

    # def partial_update(self, request, pk=None):
    #     pass

    # def destroy(self, request, pk=None):
    #     pass

    # class PostList(viewsets.ModelViewSet):
    #     permission_classes = [IsAuthenticated]
    #     queryset = Post.postobjects.all()
    #     serializer_class = PostSerializer

    # class PostDetail(viewsets.ModelViewSet, PostUserWritePermission):
    #     permission_classes = [PostUserWritePermission]
    #     queryset = Post.objects.all()
    #     serializer_class = PostSerializer
