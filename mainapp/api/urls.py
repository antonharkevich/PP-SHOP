from django.urls import path

from .api_views import (
    CategoryDetailAPIView, 
    BeerProductListAPIView, 
    BeerProductDetailAPIView, 
    CustomersListAPIView,
    CustomerDetailAPIView,
    CategoryAPIView, 
    PizzaProductAPIView,
    PizzaProductDetailAPIView,
    UserAPIView,
    UserDetailAPIView,
    CartProductAPIView,
    CartProductDetailAPIView,
    CartAPIView,
    CartDetailAPIView,
    OrderAPIView,
    OrderDetailAPIView
)


urlpatterns = [
    path('categories/', CategoryAPIView.as_view(), name='categories_list'),
    path('categories/<str:id>/', CategoryDetailAPIView.as_view(), name='category_detail'),
    path('customers/', CustomersListAPIView.as_view(), name='customers_list'),
    path('customers/<str:user>/', CustomerDetailAPIView.as_view(), name='customer_detail'),
    path('beer/', BeerProductListAPIView.as_view(), name='beer_list'),
    path('beer/<str:id>/', BeerProductDetailAPIView.as_view(), name='beer_detail'),
    path('pizza/', PizzaProductAPIView.as_view(), name='pizza_list'),
    path('pizza/<str:id>/', PizzaProductDetailAPIView.as_view(), name='pizza_detail'),
    path('orders/', OrderAPIView.as_view(), name='orders_list'),
    path('orders/<str:id>/', OrderDetailAPIView.as_view(), name='order_detail'),
    path('carts/', CartAPIView.as_view(), name='carts_list'),
    path('carts/<str:id>/', CartDetailAPIView.as_view(), name='cart_detail'),
    path('cartproducts/', CartProductAPIView.as_view(), name='cartproducts_list'),
    path('cartproducts/<str:id>/', CartProductDetailAPIView.as_view(), name='cartproduct_detail'),
    path('users/', UserAPIView.as_view(), name='users_list'),
    path('users/<str:id>/', UserDetailAPIView.as_view(), name='user_detail'),
]