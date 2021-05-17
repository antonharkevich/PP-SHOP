from collections import OrderedDict

from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from .serializers import CategorySerializer, UserSerializer, BeerProductSerializer, CustomerSerializer, PizzaProductSerializer, OrderSerializer, CartProductSerializer, CartSerializer
from ..models import Category, BeerProduct, Customer, User, CartProduct, Cart, PizzaProduct, Order

from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser, BasePermission, SAFE_METHODS
from rest_framework.response import Response

from ..custom_logging import logger

class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        logger.info('Использование функции has_permission')
        return request.method in SAFE_METHODS


class CategoryPagination(PageNumberPagination):

    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 10

    def get_paginated_response(self, data):
        logger.info('Использование PageNumberPagination')
        return Response(OrderedDict([
            ('objects_count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('items', data),
        ]))

class CategoryDetailAPIView(RetrieveAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView):

    permission_classes = [IsAuthenticated, IsAdminUser|ReadOnly]

    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = 'id'


class CategoryAPIView(ListCreateAPIView):

    permission_classes = [IsAuthenticated, IsAdminUser|ReadOnly]

    serializer_class = CategorySerializer
    pagination_class = CategoryPagination
    queryset = Category.objects.all()


class BeerProductListAPIView(ListCreateAPIView):

    permission_classes = [IsAuthenticated, IsAdminUser|ReadOnly]

    serializer_class = BeerProductSerializer
    queryset = BeerProduct.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['id', 'title', 'price', 'grade']


class BeerProductDetailAPIView(RetrieveAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView):
    
    permission_classes = [IsAuthenticated, IsAdminUser|ReadOnly]

    serializer_class = BeerProductSerializer
    queryset = BeerProduct.objects.all()
    lookup_field = 'id' 


class CustomersListAPIView(ListCreateAPIView):

    permission_classes = [IsAdminUser]

    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()


class CustomerDetailAPIView(RetrieveAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView):

    permission_classes = [IsAdminUser]

    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    lookup_field = 'user' 


class PizzaProductDetailAPIView(RetrieveAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView):

    permission_classes = [IsAuthenticated, IsAdminUser|ReadOnly]

    serializer_class = PizzaProductSerializer
    queryset = PizzaProduct.objects.all()
    lookup_field = 'id'


class PizzaProductAPIView(ListCreateAPIView):

    permission_classes = [IsAuthenticated, IsAdminUser|ReadOnly]

    serializer_class = PizzaProductSerializer
    queryset = PizzaProduct.objects.all()


class UserDetailAPIView(RetrieveAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView):

    permission_classes = [IsAdminUser]

    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'id'


class UserAPIView(ListCreateAPIView):

    permission_classes = [IsAdminUser]

    serializer_class = UserSerializer
    queryset = User.objects.all()


class CartDetailAPIView(RetrieveAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView):

    permission_classes = [IsAdminUser]

    serializer_class = CartSerializer
    queryset = Cart.objects.all()
    lookup_field = 'id'


class CartAPIView(ListCreateAPIView):

    permission_classes = [IsAdminUser]

    serializer_class = CartSerializer
    queryset = Cart.objects.all()


class CartProductDetailAPIView(RetrieveAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView):

    permission_classes = [IsAdminUser]

    serializer_class = CartProductSerializer
    queryset = CartProduct.objects.all()
    lookup_field = 'id'


class CartProductAPIView(ListCreateAPIView):

    permission_classes = [IsAdminUser]

    serializer_class = CartProductSerializer
    queryset = CartProduct.objects.all()


class OrderDetailAPIView(RetrieveAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView):

    permission_classes = [IsAdminUser]

    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    lookup_field = 'id'


class OrderAPIView(ListCreateAPIView):

    permission_classes = [IsAdminUser]

    serializer_class = OrderSerializer
    queryset = Order.objects.all()



