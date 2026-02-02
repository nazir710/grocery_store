import pytest

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from product.models import Category, Product, ShoppingCart, SubCategory


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create(
        username='testuser',
        password='testpass123',
        email='test@example.com'
    )


@pytest.fixture
def jwt_token(user):
    """Генерирует JWT токен для пользователя."""
    refresh = RefreshToken.for_user(user)
    print('refresh', refresh)
    return str(refresh.access_token)


@pytest.fixture
def user_client(user, jwt_token):
    """Клиент с JWT аутентификацией."""
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {jwt_token}')
    print('client', client)
    return client


@pytest.fixture
def category():
    return Category.objects.create(
        name='Тестовая категория',
        slug='test-category',
        image=SimpleUploadedFile(
            name='product_image.jpg',
            content=b'',
            content_type='image/jpeg'
        )
    )


@pytest.fixture
def subcategory(category):
    return SubCategory.objects.create(
        name='Тестовая подкатегория',
        slug='test-subategory',
        category=category,
        image=SimpleUploadedFile(
            name='product_image.jpg',
            content=b'',
            content_type='image/jpeg'
        )
    )


@pytest.fixture
def product(category, subcategory):
    return Product.objects.create(
        name='Название продукта',
        slug='test-product',
        price=100,
        category=category,
        subcategory=subcategory,
        image=SimpleUploadedFile(
            name='product_image.jpg',
            content=b'',
            content_type='image/jpeg'
        )
    )


@pytest.fixture
def shopping_cart_form_data(product):
    """Данные для добавления в корзину."""
    return {
        'product': product.name,
        'amount': 3
    }


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture
def shoppingcart():
    return ShoppingCart.objects.create(
        product='Название продукта',
        amount=1,
    )


@pytest.fixture
def categories_list_url():
    """URL для списка категорий."""
    return reverse('categories-list')


@pytest.fixture
def products_list_url():
    """URL для списка продуктов."""
    return reverse('products-list')


@pytest.fixture
def shopping_cart_list_url():
    """URL для списка корзины."""
    return reverse('shopping_cart-list')
