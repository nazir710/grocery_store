"""URLs для категорий, продуктов, корзины."""


from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (CategoryViewSet, ProductViewSet,
                       ShoppingCartViewSet)

router_v1 = DefaultRouter()

router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('products', ProductViewSet, basename='products')
router_v1.register(
    'shopping_cart', ShoppingCartViewSet, basename='shopping_cart'
)


urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
