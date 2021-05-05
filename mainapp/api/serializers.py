from rest_framework import serializers

from ..models import Category, BeerProduct


class CategorySerializer(serializers.ModelSerializer):

    name = serializers.CharField(required=True)
    slug = serializers.SlugField()

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'slug'
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
