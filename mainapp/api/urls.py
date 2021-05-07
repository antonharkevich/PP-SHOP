from django.urls import path

from .api_views import (
    CategoryAPIView, 
    BeerProductListAPIView, 
    BeerProductDetailAPIView, 
    CustomersListAPIView
)


urlpatterns = [
    path('categories/<str:id>/', CategoryAPIView.as_view(), name='categories_list'),
    path('customers/', CustomersListAPIView.as_view(), name='customers_list'),
    path('beer/', BeerProductListAPIView.as_view(), name='beer_list'),
    path('beer/<str:id>/', BeerProductDetailAPIView.as_view(), name='beer_detail'),

]