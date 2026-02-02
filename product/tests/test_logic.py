import pytest

from product.models import ShoppingCart


FORM_DATA = {
    'product': 'Название продукта',
    "amount": 1
}


@pytest.mark.django_db
def test_anonymous_user_cant_add_product(
    client,
    shopping_cart_form_data,
    shopping_cart_list_url
):
    """Анонимный пользователь не может добавить товар в корзину."""
    products_count_before = ShoppingCart.objects.count()
    client.post(shopping_cart_list_url, data=shopping_cart_form_data)
    products_count_after = ShoppingCart.objects.count()
    assert products_count_after == products_count_before


def test_user_can_add_product(
        user_client,
        user,
        shopping_cart_form_data,
        shopping_cart_list_url
):
    """Авторизованный пользователь может добавить товар в корзину."""
    products_count_before = ShoppingCart.objects.filter(user=user).count()
    user_client.post(shopping_cart_list_url, data=shopping_cart_form_data)
    products_count_after = ShoppingCart.objects.filter(user=user).count()
    assert products_count_after == products_count_before + 1
