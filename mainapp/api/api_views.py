from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter
from .serializers import CategorySerializer, BeerProductSerializer
from ..models import Category, BeerProduct

class CategoryListAPIView(ListAPIView):

    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class BeerProductListAPIView(ListAPIView):

    serializer_class = BeerProductSerializer
    queryset = BeerProduct.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['id', 'title', 'price']