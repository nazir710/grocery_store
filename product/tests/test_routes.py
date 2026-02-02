import pytest

from http import HTTPStatus

from django.test.client import Client


@pytest.mark.parametrize(
    'name, parametrized_client, expected_status',
    (
        (
            pytest.lazy_fixture('categories_list_url'),
            Client(),
            HTTPStatus.OK
        ),
        (
            pytest.lazy_fixture('products_list_url'),
            Client(),
            HTTPStatus.OK
        ),
        (
            pytest.lazy_fixture('shopping_cart_list_url'),
            Client(),
            HTTPStatus.UNAUTHORIZED
        ),
    )
)
def test_pages_availability(name, parametrized_client, expected_status):
    response = parametrized_client.get(name)
    assert response.status_code == expected_status
