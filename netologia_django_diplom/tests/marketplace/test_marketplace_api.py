import pytest
from django.urls import reverse
from rest_framework.status import *

from marketplace.models import *


@pytest.mark.django_db
def test_get_product(api_client, product_factory):
    # arrange
    product = product_factory()
    url = reverse('product-detail', args=(product.id,))

    # act
    resp = api_client.get(url)

    # assert
    assert resp.status_code == HTTP_200_OK
    assert resp.json()["id"] == product.id


@pytest.mark.django_db
def test_get_product_list(api_client, product_factory):
    # arrange
    product_1 = product_factory()
    product_2 = product_factory()
    url = reverse('product-list')

    # act
    resp = api_client.get(url)

    # assert
    assert resp.status_code == HTTP_200_OK

    resp_json = resp.json()
    assert len(resp_json) == 2

    resp_ids = {r["id"] for r in resp_json}
    assert resp_ids == {product_1.id, product_2.id}


@pytest.mark.django_db
def test_sort_products_by_id(api_client, product_factory):
    # arrange
    url = reverse('product-list')
    product_1 = product_factory()
    product_2 = product_factory()
    product_3 = product_factory()

    # act
    resp = api_client.get(url)
    sorted_coursers = {product_1.id, product_2.id, product_3.id}

    # assert
    assert resp.status_code == HTTP_200_OK

    resp_json = resp.json()
    resp_ids = {r["id"] for r in resp_json}
    assert resp_ids == sorted_coursers


@pytest.mark.django_db
def test_sort_courses_by_name(api_client, product_factory):
    # arrange
    url = reverse('product-list')
    product1 = product_factory(name='Computer')
    product2 = product_factory(name='Toaster')
    product3 = product_factory(name='Car')

    # act
    resp = api_client.get(url)
    sorted_products = {product1.name, product2.name, product3.name}

    # assert
    assert resp.status_code == HTTP_200_OK

    resp_json = resp.json()
    resp_ids = {r["name"] for r in resp_json}
    assert resp_ids == sorted_products
