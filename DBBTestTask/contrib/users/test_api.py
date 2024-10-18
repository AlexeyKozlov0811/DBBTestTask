# Create a TestClient using the FastAPI app
import pytest
from sqlmodel import select
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
)

from DBBTestTask.contrib.users.auth import create_access_token, hash_password
from DBBTestTask.contrib.users.models import User


class TestAuthAPI:
    @pytest.fixture(scope='class')
    def auth_urls(self):
        return {
            'register': '/api/users/register',
            'login': '/api/users/login',
            'me': '/api/users/me',
        }

    @pytest.fixture(scope='class')
    def registered_user(self, session):
        user = User(
            username="registered_username",
            hashed_password=hash_password('test_password'),
            email="registered@string",
        )
        session.add(user)
        session.commit()
        return user

    def test_register_user(self, auth_urls, client, session):
        username = "test"
        email = "string@string"

        resp = client.post(
            auth_urls['register'],
            json={
                "username": username,
                "password": "string",
                "email": email
            })
        data = resp.json()
        registered_user = session.exec(select(User).where(User.id == data['user_id'])).first()

        assert resp.status_code == HTTP_201_CREATED
        assert username == registered_user.username
        assert email == registered_user.email

    def test_register_existing_user(self, auth_urls, client, session, registered_user):
        username = "test"
        email = "<EMAIL>"

        resp = client.post(
            auth_urls['register'],
            json={
                "username": username,
                "password": "string",
                "email": email
            })

        assert resp.status_code == HTTP_400_BAD_REQUEST

    def test_login_user(self, auth_urls, client, session, registered_user):
        resp = client.post(
            auth_urls['login'],
            data={"grant_type": "password", "username": registered_user.username, "password": 'test_password'})

        data = resp.json()
        assert resp.status_code == HTTP_200_OK
        assert data['access_token'] == create_access_token(data={"sub": registered_user.username})

    def test_login_with_incorrect_credentials(self, auth_urls, client, session, registered_user):
        resp = client.post(
            auth_urls['login'],
            data={"grant_type": "password", "username": 'wrong_username', "password": 'wrong_password'})

        assert resp.status_code == HTTP_401_UNAUTHORIZED
