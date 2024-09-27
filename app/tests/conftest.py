import pytest
from rest_framework.test import APIClient
from django.conf import settings
from cryptography.fernet import Fernet
from app.password_service.models import ServicePassword


@pytest.fixture
def api_client():

    return APIClient()


@pytest.fixture(scope='session')
def encryption_key():

    return settings.ENCRYPTION_KEY


@pytest.fixture
def create_service_password(encryption_key):

    def create(service_name, password):
        encrypted_password = Fernet(encryption_key).encrypt(password.encode())
        return ServicePassword.objects.create(service_name=service_name, password=encrypted_password)
    return create
