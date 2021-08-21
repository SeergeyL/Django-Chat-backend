import pytest
from django.contrib.auth.models import User


def test_me_not_auth(client):
    response = client.get('/api/v1/me/')

    assert response.status_code != 404, 'Страница `/api/v1/me/` не найдена'

    assert response.status_code == 401, \
        "Доступ к `/api/v1/me/` при GET запросе без токена запрещён"


def test_users_not_auth(client):
    response = client.get('/api/v1/users/')

    assert response.status_code != 404, "Страница `/api/v1/users/` не найдена"

    assert response.status_code == 401, \
        "Доступ к `/api/v1/users/` при GET запросе без токена запрещён"


@pytest.mark.django_db(transaction=True)
def test_register(client):
    user_data = {}
    response = client.post('/api/v1/register/', user_data)

    assert response.status_code != 404, "Страница `/api/v1/register/` не найдена"

    assert response.status_code == 400, \
        "При POST запросе к `/api/v1/register/` с неверными данными должен " \
        "возвращаться статус код 400"

    user_data = {
        'username': 'new_username',
        'password': 'test123456'
    }
    response = client.post('/api/v1/register/', user_data)
    assert response.status_code == 400, \
        "При POST запросе к `/api/v1/register/` с неверными данными должен " \
        "возвращаться статус код 400"

    user_data = {
        'username': 'new_username',
        'password': 'test123456',
        'password2': 'test123456'
    }
    response = client.post('/api/v1/register/', user_data)
    assert response.status_code == 400, \
        "При POST запросе к `/api/v1/register/` с неверными данными должен " \
        "возвращаться статус код 400"

    user_data = {
        'username': 'new_username',
        'email': 'test@test.ru',
        'password': 'test123456',
        'password2': '123456'
    }
    response = client.post('/api/v1/register/', user_data)
    assert response.status_code == 400, \
        "При POST запросе к `/api/v1/register/` с неверными данными должен " \
        "возвращаться статус код 400"

    user_data = {
        'username': 'new_username',
        'email': 'test@test.ru',
        'password': '123456',
        'password2': '123456'
    }
    response = client.post('/api/v1/register/', user_data)
    assert response.status_code == 400, \
        "При POST запросе к `/api/v1/register/` с неверными данными должен " \
        "возвращаться статус код 400"

    user_data = {
        'username': 'new_username',
        'email': 'test@test.ru',
        'password': 'test123456',
        'password2': 'test123456',
    }
    response = client.post('/api/v1/register/', user_data)
    assert response.status_code == 201, \
        "При успешном POST запросе к `/api/v1/register/` " \
        "должен возвращаться статус код 201"

    count = User.objects.count()

    assert count == 1, \
        "При POST запросе к `/api/v1/register/` в базе данных должен " \
        "создаться пользователь"


@pytest.mark.django_db(transaction=True)
def test_get_auth(client):
    user_data = {
        'username': 'new_username',
        'email': 'test@test.ru',
        'password': 'test123456',
        'password2': 'test123456',
    }
    client.post('/api/v1/register/', user_data)

    user_data = {'username': 'new_username', 'password': 'test'}
    response = client.post('/api/v1/api-token-auth/', user_data)

    assert response.status_code != 404, "Страница `/api/v1/api-token-auth/` не найдена"

    assert response.status_code == 400, \
        "При POST запросе к `/api/v1/api-token-auth/` " \
        "с неверными данными должен возвращаться статус код 400"

    user_data = {'username': 'new', 'password': 'test123456'}
    response = client.post('/api/v1/api-token-auth/', user_data)

    assert response.status_code == 400, \
        "При POST запросе к `/api/v1/api-token-auth/` " \
        "с неверными данными должен возвращаться статус код 400"

    user_data = {'username': 'new_username', 'password': 'test123456'}
    response = client.post('/api/v1/api-token-auth/', user_data)

    assert response.status_code == 200, \
        "При успешном POST запросе к `/api/v1/api-token-auth/` " \
        "должен возвращаться статус код 200"

    data = response.json()
    assert data['token'], \
        "При успешном POST запросе к `/api/v1/api-token-auth/` в теле запроса " \
        "должен быть `token`"



