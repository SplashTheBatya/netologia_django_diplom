import pytest
from django.urls import reverse
from rest_framework.status import *


@pytest.mark.django_db
def test_user_get_order(api_client, order_factory, get_or_create_user_token):
    # arrange
    user = get_or_create_user_token.user
    order = order_factory(user=user)
    user_token = get_or_create_user_token
    url = reverse('order-detail', args=(order.id,))
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + user_token.key)

    # act
    resp = api_client.get(url, user=user)

    # assert
    assert resp.status_code == HTTP_200_OK
    assert resp.json()["id"] == order.id


@pytest.mark.django_db
def test_user_get_order_list(api_client, order_factory, get_or_create_user_token):
    # arrange
    user = get_or_create_user_token.user
    user_token = get_or_create_user_token

    url = reverse('order-list')
    order_1 = order_factory(user=user)
    order_2 = order_factory()
    order_3 = order_factory()

    api_client.credentials(HTTP_AUTHORIZATION='Token ' + user_token.key)

    # act
    resp = api_client.get(url)

    # assert
    assert resp.status_code == HTTP_200_OK

    resp_json = resp.json()
    assert len(resp_json) == 1

    resp_ids = {r["id"] for r in resp_json}
    assert resp_ids == {order_1.id}


@pytest.mark.django_db
def test_admin_get_order_list(api_client, order_factory, get_or_create_admin_token):
    # arrange
    url = reverse('order-list')
    order_1 = order_factory()
    order_2 = order_factory()
    order_3 = order_factory()

    admin = api_client
    admin_token = get_or_create_admin_token

    admin.credentials(HTTP_AUTHORIZATION='Token ' + admin_token.key)

    # act
    resp = admin.get(url)

    # assert
    assert resp.status_code == HTTP_200_OK

    resp_json = resp.json()
    assert len(resp_json) == 3

    resp_ids = {r["id"] for r in resp_json}
    assert resp_ids == {order_1.id, order_2.id, order_3.id}


@pytest.mark.django_db
def test_user_patch_order(api_client, order_factory, get_or_create_user_token):
    # arrange
    user = get_or_create_user_token.user
    user_token = get_or_create_user_token

    api_client.credentials(HTTP_AUTHORIZATION='Token ' + user_token.key)
    order = order_factory(user=user)
    url = reverse('order-detail', args=(order.id,))
    payload = {
        "status": "DONE"
    }

    # act
    resp = api_client.patch(url, payload, format="json", user=user)
    resp_json = resp.json()
    expected_rating = payload["status"]

    # assert
    assert resp.status_code == HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_admin_patch_order(api_client, order_factory, get_or_create_admin_token):
    # arrange
    order = order_factory()
    url = reverse('order-detail', args=(order.id,))

    admin = api_client
    admin_token = get_or_create_admin_token

    admin.credentials(HTTP_AUTHORIZATION='Token ' + admin_token.key)
    payload = {
        "status": "DONE"
    }

    # act
    resp = api_client.patch(url, payload, format="json")
    resp_json = resp.json()
    expected_status = payload["status"]

    # assert
    assert resp.status_code == HTTP_200_OK
    assert resp_json["status"] == expected_status


@pytest.mark.django_db
def test_destroy_order(api_client, order_factory, get_or_create_user_token):
    # arrange
    user = get_or_create_user_token.user
    order = order_factory(user=user)
    url = reverse('order-detail', args=(order.id,))

    user_token = get_or_create_user_token
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + user_token.key)

    # act
    resp = api_client.delete(url)

    # assert
    assert resp.status_code == HTTP_204_NO_CONTENT

