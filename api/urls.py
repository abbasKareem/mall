from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter


# from .views import ListProductView, ListMyOrderView, RegisterAPIView, OrderCreateView, DetailOrderView, ListProductByShopName, ListProductByViewCountName, DetailProductView, ListCategoryView, ListProductsByCategoryIdView,  LowProductView, HighProductView, ProductReviewView, ListProductReviewView
from .views import *


urlpatterns = [
    # Products
    path('products/', ListProductView.as_view()),
    path('products/shop/<str:name>', ListProductByShopName.as_view()),
    path('products/view_count', ListProductByViewCountName.as_view()),
    path('products/<int:pk>', DetailProductView.as_view()),
    path('products/price/low', LowProductView.as_view()),
    path('products/price/high', HighProductView.as_view()),
    path('products/review/<int:pk>', ProductReviewView.as_view()),

    # Shops
    path('shops/', ListAllShopView.as_view()),

    # WishList
    path('wishlist/create', WishListCreateView.as_view()),
    path('wishlist/', AllWishListView.as_view()),
    path('wishlist/<int:id>', DeleteWishListView.as_view()),


    # Category
    path('categories', ListCategoryView.as_view()),
    path('categories/<int:pk>', ListProductsByCategoryIdView.as_view()),

    # orders
    path('api/orders/', ListMyOrderView.as_view()),
    path('api/orders/<int:pk>', DetailOrderView.as_view()),
    path('api/orders/create/', OrderCreateView.as_view()),
    path('register', RegisterAPIView.as_view(), name="register")
]
