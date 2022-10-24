from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter


# from .views import ListProductView, ListMyOrderView, RegisterAPIView, OrderCreateView, DetailOrderView, ListProductByShopName, ListProductByViewCountName, DetailProductView, ListCategoryView, ListProductsByCategoryIdView,  LowProductView, HighProductView, ProductReviewView, ListProductReviewView
from .views import *


urlpatterns = [
    # Products
    path('', index, name='homepage'),
    path('products/', ListProductView.as_view()),
    path('products/<str:query>/', SearchProductView.as_view()),

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


    # Followers
    path('follow/create', FollowersCreateView.as_view()),
    path('follow/', AllFollowersView.as_view()),
    path('follow/<str:shop_name>', UnfollowView.as_view()),


    # Category
    path('categories', ListCategoryView.as_view()),
    path('categories/<int:pk>', ListProductsByCategoryIdView.as_view()),

    # orders
    path('api/add-to-cart', AddToCartView.as_view()),
    path('api/orders/', ListMyOrderView.as_view()),
    path('api/orders/<int:pk>', DetailOrderView.as_view()),
    path('api/orders/create/', OrderCreateView.as_view()),
    path('register', RegisterAPIView.as_view(), name="register"),

    path('api/complaint', ComplaintCreateView.as_view()),



    # profile
    path('api/user/me', ProfileView.as_view()),
    path('api/user/me/change/password', ChangePasswordView.as_view()),

    path('activate/<str:uid>/<str:token>',
         user_activate_account, name='user_activate_account'),
    path('activate/success', user_activate_account_succcess,
         name='user_activate_account_succcess'),
    path('password/reset/confirm/<str:uid>/<str:token>',
         reset_user_password, name='reset_user_password'),
    path('password/success', reset_password_success,
         name='reset_password_success')
]
