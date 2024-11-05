from fastapi.testclient import TestClient
import pytest

from shopping_cart_api.app import app

@pytest.fixture()
def client():
    with TestClient(app) as client:
        yield client