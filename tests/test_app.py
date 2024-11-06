import json
from http import HTTPStatus
from unittest.mock import patch

from fastapi.testclient import TestClient

from shopping_cart_api.app import OrderSchema


def test_root(client: TestClient):
    response = client.get("/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Hi! 👋👋👋"}


def test_create_order(client: TestClient):
    order = OrderSchema(
        buyer_id=1,
        product_id=1,
        number_of_installments=12,
        total_amount=10.000,
        purchase_date="2024-11-05",
    )

    with patch("boto3.client") as mock_sns_client:
        mock_sns_client.publish = {"MessageId": "11111", "SequenceNumber": "11111"}
        response = client.post("/order/", json=json.loads(order.model_dump_json()))

    result_order = OrderSchema.model_validate(response.json())

    assert response.status_code == HTTPStatus.CREATED
    assert result_order.uuid is not None
    assert (
        result_order.buyer_id == order.buyer_id
        and result_order.product_id == order.product_id
        and result_order.number_of_installments == order.number_of_installments
        and result_order.total_amount == order.total_amount
        and result_order.purchase_date == order.purchase_date
    )


def test_create_order_failing(client: TestClient):
    order = OrderSchema(
        buyer_id=1,
        product_id=1,
        number_of_installments=12,
        total_amount=10.000,
        purchase_date="2024-11-05",
    )
    response = client.post("/order/", json=json.loads(order.model_dump_json()))
    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
