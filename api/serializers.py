"Сериализаторы."

from django.shortcuts import get_object_or_404

from rest_framework import serializers

from api.fields import Base64ImageField
from product.constants import Constants
from product.models import Category, Product, ShoppingCart


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""

    name = serializers.CharField(
        max_length=Constants.category_name_max_length,
        read_only=True
    )
    slug = serializers.CharField(
        max_length=Constants.slug_max_length,
        read_only=True
    )
    subcategories = serializers.StringRelatedField(many=True, read_only=True)
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        fields = ('id', 'name', 'slug', 'image', 'subcategories')
        model = Category


class ProductImageSerializer(serializers.Serializer):
    """Сериализатор для изображений в разных размерах."""
    original = serializers.ImageField(source='image')
    small = serializers.ImageField(source='image_small')
    medium = serializers.ImageField(source='image_medium')
    large = serializers.ImageField(source='image_large')


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для продуктов."""
    images = ProductImageSerializer(source='*', read_only=True)

    class Meta:
        fields = (
            'id',
            'name',
            'slug',
            'images',
            'price',
            'category',
            'subcategory'
        )
        model = Product


class ShoppingCartPostSerializer(serializers.ModelSerializer):

    product = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Product.objects.all()
    )

    class Meta:
        fields = (
            'product',
            'amount'
        )
        model = ShoppingCart

    def create(self, validated_data):
        product_name = validated_data.pop('product')
        product = get_object_or_404(Product, name=product_name)
        return ShoppingCart.objects.create(
            user=self.context['request'].user,
            product=product,
            amount=validated_data['amount']
        )

    def validate_product(self, product):
        if not Product.objects.filter(name=product).exists():
            raise serializers.ValidationError(
                'Продукта с таким названием не существует.'
            )
        return product

    def validate_amount(self, amount):
        if not isinstance(amount, int):
            raise serializers.ValidationError(
                'Количество продукта должно быть целым числом.'
            )
        return amount


class ShoppingCartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_total_price = serializers.SerializerMethodField()

    class Meta:
        model = ShoppingCart
        fields = ['id', 'product', 'amount', 'product_total_price']

    def get_product_total_price(self, obj):
        return obj.amount * obj.product.price
