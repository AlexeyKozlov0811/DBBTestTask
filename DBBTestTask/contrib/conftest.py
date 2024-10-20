
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from db import get_session
from DBBTestTask.contrib.users.auth import create_access_token, hash_password
from DBBTestTask.contrib.users.models import User
from main import app


@pytest.fixture(name="session")
def session_fixture() -> Session:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session: Session) -> TestClient:
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

@pytest.fixture(name='user')
def registered_user(session: Session) -> User:
    user = User(
        username="registered_username",
        hashed_password=hash_password('test_password'),
        email="registered@string",
    )
    session.add(user)
    session.commit()
    yield user

@pytest.fixture(name='client_logged')
def authenticated_client(user: User, session: Session) -> TestClient:
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app, headers={'Authorization': f'Bearer {create_access_token(data={"sub": user.username})}'})
    yield client
    app.dependency_overrides.clear()
