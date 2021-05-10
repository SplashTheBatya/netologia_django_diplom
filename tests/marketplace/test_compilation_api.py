import pytest
from django.urls import reverse
from rest_framework.status import *
from marketplace.models import *


@pytest.mark.django_db
def test_get_compilations(api_client, compilation_factory):
    # arrange
    compilation = compilation_factory()
    url = reverse('compilation-detail', args=(compilation.id,))

    # act
    resp = api_client.get(url)

    # assert
    assert resp.status_code == HTTP_200_OK
    assert resp.json()["id"] == compilation.id


@pytest.mark.django_db
def test_get_compilation_list(api_client, compilation_factory):
    # arrange
    compilation_1 = compilation_factory()
    compilation_2 = compilation_factory()
    url = reverse('compilation-list')

    # act
    resp = api_client.get(url)

    # assert
    assert resp.status_code == HTTP_200_OK

    resp_json = resp.json()
    assert len(resp_json) == 2

    resp_ids = {r["id"] for r in resp_json}
    assert resp_ids == {compilation_1.id, compilation_2.id}


@pytest.mark.django_db
def test_admin_post_compilation(api_client, get_or_create_admin_token, product_factory):
    # arrange
    admin_token = get_or_create_admin_token
    admin = api_client
    product_1, _ = Product.objects.get_or_create(product_factory())

    admin.credentials(HTTP_AUTHORIZATION='Token ' + admin_token.key)
    url = reverse('compilation-list')
    payload = {
        "heading": "Compilation 5",
        "description": "Some compilation bla bla bla",
        "product": [product_1.id]
    }

    # act
    compilations_count = Compilation.objects.count()
    resp = admin.post(url, payload, format="json")

    # assert
    assert resp.status_code == HTTP_201_CREATED
    assert Compilation.objects.count() > compilations_count


@pytest.mark.django_db
def test_user_post_compilation(api_client, get_or_create_user_token, product_factory):
    # arrange
    url = reverse('compilation-list')
    product_1, _ = Product.objects.get_or_create(product_factory())

    user_token = get_or_create_user_token
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + user_token.key)
    payload = {
        "heading": "Compilation 5",
        "description": "Some compilation bla bla bla",
        "product": [product_1.id]
    }

    # act
    resp = api_client.post(url, payload, format="json")

    # assert
    assert resp.status_code == HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_admin_destroy_compilation(api_client, get_or_create_admin_token, compilation_factory):
    # arrange
    compilation = compilation_factory()
    admin = api_client
    admin_token = get_or_create_admin_token

    admin.credentials(HTTP_AUTHORIZATION='Token ' + admin_token.key)
    url = reverse('compilation-detail', args=(compilation.id,))

    # act
    resp = api_client.delete(url)

    # assert
    assert resp.status_code == HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_user_destroy_compilation(api_client, get_or_create_user_token, compilation_factory):
    # arrange
    compilation = compilation_factory()
    user = api_client
    admin_token = get_or_create_user_token

    user.credentials(HTTP_AUTHORIZATION='Token ' + admin_token.key)
    url = reverse('compilation-detail', args=(compilation.id,))

    # act
    resp = api_client.delete(url)

    # assert
    assert resp.status_code == HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_admin_patch_compilation(api_client, get_or_create_admin_token, product_factory, compilation_factory):
    # arrange
    admin_token = get_or_create_admin_token
    admin = api_client
    product_1, _ = Product.objects.get_or_create(product_factory())
    compilation = compilation_factory()

    admin.credentials(HTTP_AUTHORIZATION='Token ' + admin_token.key)
    url = reverse('compilation-detail', args=(compilation.id, ))
    payload = {
        "product": [product_1.id]
    }

    # act
    resp = admin.patch(url, payload, format="json")

    # assert
    assert resp.status_code == HTTP_200_OK


@pytest.mark.django_db
def test_user_patch_compilation(api_client, get_or_create_user_token, product_factory, compilation_factory):
    # arrange
    product_1, _ = Product.objects.get_or_create(product_factory())
    compilation = compilation_factory()
    url = reverse('compilation-detail', args=(compilation.id, ))

    user_token = get_or_create_user_token
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + user_token.key)
    payload = {
        "product": [product_1.id]
    }

    # act
    resp = api_client.patch(url, payload, format="json")

    # assert
    assert resp.status_code == HTTP_403_FORBIDDEN