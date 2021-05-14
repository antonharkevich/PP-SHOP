from rest_framework import serializers

from ..models import Category, BeerProduct, Customer, User, CartProduct, Cart, PizzaProduct, Order
from ..custom_logging import logger

class CategorySerializer(serializers.ModelSerializer):

    name = serializers.CharField(required=True)
    slug = serializers.SlugField()

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'slug'
        ]



class UserSerializer(serializers.ModelSerializer):

    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    

    class Meta:
        model = User
        fields = [
            'id', 'first_name', 'last_name', 'username', 'email'
        ]


class BaseProductSerializer:

    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects)
    title = serializers.CharField(required=True)
    slug = serializers.SlugField(required=True)
    image = serializers.ImageField(required=True)
    description = serializers.CharField(required=False)
    price = serializers.DecimalField(max_digits=9, decimal_places=2, required=True)
    


class BeerProductSerializer(BaseProductSerializer, serializers.ModelSerializer):

    colour = serializers.CharField(required=True)
    alcohol_strength = serializers.CharField(required=True) 
    filtered = serializers.CharField(required=True)
    grade = serializers.CharField(required=True)

    class Meta:
        model = BeerProduct
        fields = '__all__'
    

        


class PizzaProductSerializer(BaseProductSerializer, serializers.ModelSerializer):

    size = serializers.CharField(required=True)
    board = serializers.CharField(required=True) 
    dough = serializers.CharField(required=True)
    vegetarian = serializers.BooleanField(required=True)

    class Meta:
        model = PizzaProduct
        fields = '__all__'



class OrderSerializer(serializers.ModelSerializer):


    class Meta:
        model = Order
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):

    orders = OrderSerializer(many=True)
    user = UserSerializer()
    
    class Meta:
        model = Customer
        fields = '__all__'
    
    def create(self, validated_data):
        logger.warning('Создание нового объекта customer через api')
        user_data = validated_data.pop('user')
        orders_data = validated_data.pop('orders')
        user = User.objects.get(username=user_data["username"])
        customer = Customer.objects.create(user=user, **validated_data)
        return customer
    
    def update(self, instance, validated_data):
        logger.warning('Изменение объекта customer через api')
        instance.phone = validated_data.get('phone', instance.phone)
        instance.address = validated_data.get('address', instance.address)
        instance.save()
        return instance


class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = '__all__'


class CartProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartProduct
        fields = '__all__'