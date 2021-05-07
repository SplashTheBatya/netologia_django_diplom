import pytest
from django.contrib.auth.models import User
from model_bakery import baker
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def get_or_create_admin_token(db, admin_user):
    user = admin_user
    token, _ = Token.objects.get_or_create(user=user)
    return token


@pytest.fixture
def get_or_create_user_token(db, api_client):
    user = User.objects.create()
    token, _ = Token.objects.get_or_create(user=user)
    return token


@pytest.fixture
def product_factory():
    def factory(**kwargs):
        return baker.make('marketplace.Product', **kwargs)

    return factory


@pytest.fixture
def review_factory():
    def factory(**kwargs):
        return baker.make('marketplace.Review', **kwargs)

    return factory
