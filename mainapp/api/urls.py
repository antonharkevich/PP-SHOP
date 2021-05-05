from django.urls import path

from .api_views import CategoryListAPIView, BeerProductListAPIView

urlpatterns = [
    path('categories/', CategoryListAPIView.as_view(), name='categories'),
    path('beer/', BeerProductListAPIView.as_view(), name='beer'),
]