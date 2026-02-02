"""Представления."""

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from api.permissions import IsAuthenticatedAndIsInSaveMethodsPermission
from api.serializers import (CategorySerializer,
                             ProductSerializer,
                             ShoppingCartItemSerializer,
                             ShoppingCartPostSerializer)
from product.models import Category, Product, ShoppingCart


class CategoryViewSet(viewsets.ModelViewSet):
    """Представления для категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    http_method_names = ['get']
    pagination_class = LimitOffsetPagination


class ProductViewSet(viewsets.ModelViewSet):
    """Представления для категорий."""

    queryset = Product.objects.select_related('subcategory')
    serializer_class = ProductSerializer
    http_method_names = ['get']
    pagination_class = LimitOffsetPagination


class ShoppingCartViewSet(viewsets.ModelViewSet):
    """Представления для категорий."""

    permission_classes = (IsAuthenticatedAndIsInSaveMethodsPermission,)
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return ShoppingCartItemSerializer
        return ShoppingCartPostSerializer

    def perform_create(self, serializer):
        """Переопределяем метод для добавления продукта в корзину."""
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def my_cart(self, request):
        """Вся корзина пользователя."""
        products = ShoppingCart.objects.filter(user=request.user)
        products_serializer = ShoppingCartItemSerializer(products, many=True)
        total_price = sum(
            item.amount * item.product.price for item in products
        )
        total_amount = sum(item.amount for item in products)
        return Response({
            'products': products_serializer.data,
            'total_price': total_price,
            'total_amount': total_amount
        })

    @action(detail=False, methods=['delete'])
    def clear_cart(self, request):
        """Очистка всей корзины пользователя."""
        ShoppingCart.objects.filter(
            user=request.user
        ).delete()
        return Response(
            {'result': 'Корзина пуста'},
            status=status.HTTP_204_NO_CONTENT
        )
