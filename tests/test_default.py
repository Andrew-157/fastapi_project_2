from fastapi import status
from fastapi.testclient import TestClient


def test_root(client: TestClient):
    response = client.get('/')
    assert response.status_code == status.HTTP_200_OK
    expected_json = {"is_root": True}
    assert response.json() == expected_json
