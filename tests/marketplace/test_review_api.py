import pytest
from django.urls import reverse
from rest_framework.status import *
from marketplace.models import *


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
def test_owner_patch_review(api_client, review_factory, get_or_create_user_token):
    # arrange
    user = get_or_create_user_token.user
    review = review_factory(user=user)
    user_token = get_or_create_user_token
    url = reverse('review-detail', args=(review.id,))
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + user_token.key)
    payload = {
        "rating": 3
    }

    # act
    resp = api_client.patch(url, payload, format="json", user=user)
    resp_json = resp.json()
    expected_rating = payload["rating"]

    # assert
    assert resp.status_code == HTTP_200_OK
    assert resp_json["rating"] == expected_rating


@pytest.mark.django_db
def test_someone_else_patch_review(api_client, review_factory, get_or_create_user_token):
    # arrange
    user = api_client
    review = review_factory()
    user_token = get_or_create_user_token
    url = reverse('review-detail', args=(review.id,))
    user.credentials(HTTP_AUTHORIZATION='Token ' + user_token.key)
    payload = {
        "rating": 3
    }

    # act
    resp = user.patch(url, payload, format="json")
    resp_json = resp.json()
    expected_rating = payload["rating"]

    # assert
    assert resp.status_code == HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_owner_destroy_review(api_client, review_factory, get_or_create_user_token):
    # arrange
    user = get_or_create_user_token.user
    review = review_factory(user=user)
    user_token = get_or_create_user_token
    url = reverse('review-detail', args=(review.id,))
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + user_token.key)

    # act
    resp = api_client.delete(url)

    # assert
    assert resp.status_code == HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_someone_else_destroy_review(api_client, review_factory, get_or_create_user_token):
    # arrange
    user = api_client
    review = review_factory()
    user_token = get_or_create_user_token
    url = reverse('review-detail', args=(review.id,))
    user.credentials(HTTP_AUTHORIZATION='Token ' + user_token.key)

    # act
    resp = user.delete(url)

    # assert
    assert resp.status_code == HTTP_403_FORBIDDEN
