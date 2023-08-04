from fastapi.testclient import TestClient
from fastapi import status
from sqlmodel import Session, select

from app.models import User


def test_register(client: TestClient, session: Session):
    response = client.post(
        '/auth/register',
        json={"username": "user1",
              "email": "user1@gmail.com",
              "password": "34somepassword34"}
    )
    assert response.status_code == status.HTTP_201_CREATED
    user = session.exec(select(User).where(User.username == "user1")).first()
    assert user is not None
