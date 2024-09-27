import pytest
from rest_framework import status
from django.urls import reverse
from app.password_service.models import ServicePassword


@pytest.mark.django_db
@pytest.mark.parametrize("service_name, password", [
    ("test_service", "my_secret_password"),
    ("another_service", "another_password"),
])
def test_create_password(api_client, service_name, password):
    url = reverse('password_detail', args=[service_name])
    data = {'password': password}
    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
@pytest.mark.parametrize("service_name, password", [
    ("test_service", "initial_password"),
    ("another_service", "initial_password"),
])
def test_update_password(api_client, create_service_password, service_name, password):
    create_service_password(service_name, password)

    url = reverse('password_detail', args=[service_name])
    new_password = "my_updated_password"
    response = api_client.post(url, {'password': new_password})

    assert response.status_code == status.HTTP_200_OK
    assert ServicePassword.objects.get(service_name=service_name).password.tobytes() != password.encode()


@pytest.mark.django_db
@pytest.mark.parametrize("service_name, expected_password", [
    ("test_service", "my_secret_password"),
    ("another_service", "another_password"),
])
def test_get_password(api_client, create_service_password, service_name, expected_password):
    create_service_password(service_name, expected_password)

    url = reverse('password_detail', args=[service_name])
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['service_name'] == service_name
    assert response.data['password'] == expected_password


@pytest.mark.django_db
def test_get_nonexistent_password(api_client):
    url = reverse('password_detail', args=['nonexistent_service'])
    response = api_client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
@pytest.mark.parametrize("service_name, search_service, password",[
    ("service_one", "service_on", "my_password_one"),
    ("service_two", "service_t", "my_password_two"),
])
def test_search_passwords(api_client, create_service_password, service_name, search_service, password):
    create_service_password(service_name, password)

    url = reverse('search_password')
    response = api_client.get(url, {'service_name': search_service})

    assert len(response.data) == 1
    assert response.data[0]['service_name'] == service_name


@pytest.mark.django_db
def test_search_no_results(api_client):
    url = reverse('search_password')
    response = api_client.get(url, {'service_name': 'nonexistent'})

    assert len(response.data) == 0
