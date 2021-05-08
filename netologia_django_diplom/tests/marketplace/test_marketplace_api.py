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
    sorted_products = {product_1.id, product_2.id, product_3.id}

    # assert
    assert resp.status_code == HTTP_200_OK

    resp_json = resp.json()
    resp_ids = {r["id"] for r in resp_json}
    assert resp_ids == sorted_products


@pytest.mark.django_db
def test_sort_products_by_name(api_client, product_factory):
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


@pytest.mark.django_db
def test_admin_post_product(api_client, get_or_create_admin_token):
    # arrange
    admin_token = get_or_create_admin_token
    admin = api_client

    admin.credentials(HTTP_AUTHORIZATION='Token ' + admin_token.key)
    url = reverse('product-list')
    payload = {
        "name": "Product5",
        "description": "Some product bla bla bla",
        "price": 5000
    }

    # act
    product_count = Product.objects.count()
    resp = admin.post(url, payload, format="json")

    # assert
    assert resp.status_code == HTTP_201_CREATED
    assert Product.objects.count() > product_count


@pytest.mark.django_db
def test_user_post_product(api_client, get_or_create_user_token):
    # arrange
    user = api_client
    user_token = get_or_create_user_token

    user.credentials(HTTP_AUTHORIZATION='Token ' + user_token.key)
    url = reverse('product-list')
    payload = {
        "name": "Product6",
        "description": "Some product bla bla bla",
        "price": 50000
    }

    # act
    product_count = Product.objects.count()
    resp = user.post(url, payload, format="json")

    # assert
    assert resp.status_code == HTTP_403_FORBIDDEN
    assert product_count == Product.objects.count()


@pytest.mark.django_db
def test_admin_patch_product(api_client, get_or_create_admin_token, product_factory):
    # arrange
    product = product_factory()
    admin = api_client
    admin_token = get_or_create_admin_token

    admin.credentials(HTTP_AUTHORIZATION='Token ' + admin_token.key)
    url = reverse('product-detail', args=(product.id,))
    payload = {
        "name": "Amazing Product"
    }

    # act
    resp = api_client.patch(url, payload, format="json")
    resp_json = resp.json()
    expected_name = payload["name"]

    # assert
    assert resp.status_code == HTTP_200_OK
    assert resp_json["name"] == expected_name


@pytest.mark.django_db
def test_user_patch_product(api_client, get_or_create_user_token, product_factory):
    # arrange
    product = product_factory()
    user = api_client
    user_token = get_or_create_user_token

    user.credentials(HTTP_AUTHORIZATION='Token ' + user_token.key)
    url = reverse('product-detail', args=(product.id,))
    payload = {
        "name": "Very Amazing Product"
    }

    # act
    resp = api_client.patch(url, payload, format="json")
    resp_json = resp.json()
    expected_name = payload["name"]

    # assert
    assert resp.status_code == HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_admin_destroy_product(api_client, get_or_create_admin_token, product_factory):
    # arrange
    product = product_factory()
    admin = api_client
    admin_token = get_or_create_admin_token

    admin.credentials(HTTP_AUTHORIZATION='Token ' + admin_token.key)
    url = reverse('product-detail', args=(product.id,))

    # act
    resp = api_client.delete(url)

    # assert
    assert resp.status_code == HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_user_destroy_product(api_client, get_or_create_user_token, product_factory):
    # arrange
    product = product_factory()
    user = api_client
    user_token = get_or_create_user_token

    user.credentials(HTTP_AUTHORIZATION='Token ' + user_token.key)
    url = reverse('product-detail', args=(product.id,))

    # act
    resp = api_client.delete(url)

    # assert
    assert resp.status_code == HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_get_review(api_client, review_factory):
    # arrange
    review = review_factory()
    url = reverse('review-detail', args=(review.id,))

    # act
    resp = api_client.get(url)

    # assert
    assert resp.status_code == HTTP_200_OK
    assert resp.json()["id"] == review.id


@pytest.mark.django_db
def test_get_review_list(api_client, review_factory):
    # arrange
    review_1 = review_factory()
    review_2 = review_factory()
    url = reverse('review-list')

    # act
    resp = api_client.get(url)

    # assert
    assert resp.status_code == HTTP_200_OK

    resp_json = resp.json()
    assert len(resp_json) == 2

    resp_ids = {r["id"] for r in resp_json}
    assert resp_ids == {review_1.id, review_2.id}


@pytest.mark.django_db
def test_sort_reviews_by_id(api_client, review_factory):
    # arrange
    url = reverse('review-list')
    review_1 = review_factory()
    review_2 = review_factory()
    review_3 = review_factory()

    # act
    resp = api_client.get(url)
    sorted_reviews = {review_1.id, review_2.id, review_3.id}

    # assert
    assert resp.status_code == HTTP_200_OK

    resp_json = resp.json()
    resp_ids = {r["id"] for r in resp_json}
    assert resp_ids == sorted_reviews


@pytest.mark.django_db
def test_post_review(api_client, product_factory, get_or_create_user_token):
    # arrange
    product, _ = Product.objects.get_or_create(product_factory())
    url = url = reverse('review-list')
    user = api_client
    user_token = get_or_create_user_token
    user.credentials(HTTP_AUTHORIZATION='Token ' + user_token.key)
    payload = {
        "product": product.id,
        "review_text": "bla bla bla",
        "rating": 5
    }

    # act
    review_count = Review.objects.count()
    resp = user.post(url, payload, format="json")

    # assert
    assert resp.status_code == HTTP_201_CREATED
    assert Review.objects.count() > review_count


@pytest.mark.django_db
def test_patch_review(api_client, review_factory, get_or_create_user_token):
    # arrange
    user = api_client
    review = review_factory()
    user_token = get_or_create_user_token
    url = reverse('product-detail', args=(review.id,))
    user.credentials(HTTP_AUTHORIZATION='Token ' + user_token.key)
    payload = {
        "rating": 3
    }

    # act
    resp = api_client.patch(url, payload, format="json")
    resp_json = resp.json()
    expected_rating = payload["rating"]

    # assert
    assert resp.status_code == HTTP_403_FORBIDDEN
