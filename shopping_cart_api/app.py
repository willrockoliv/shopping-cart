import logging
import uuid
from http import HTTPStatus

import boto3
from fastapi import FastAPI, HTTPException
from mangum import Mangum

from shopping_cart_api.schemas import OrderSchema
from shopping_cart_api.settings import Settings

app = FastAPI()
handler = Mangum(app)


def send_sns_message(json_message: str):
    client = boto3.client("sns")
    targetArn = Settings().SNS_TARGET_ARN

    logging.info(f"""
        Sending message to SNS:
            - TargetArn: {targetArn}
            - Message: {json_message}
    """)

    response = client.publish(
        TargetArn=targetArn,
        Message=json_message,
        MessageStructure="json",
    )
    return response


@app.get("/")
async def hello_world():
    return {"message": "Hi! 👋👋👋"}


@app.post("/order/", status_code=HTTPStatus.CREATED, response_model=OrderSchema)
async def create_order(order: OrderSchema):
    if not order.uuid:
        order.uuid = uuid.uuid4()

    try:
        send_sns_message(order.model_dump_json())
    except Exception as e:
        logging.error(f"SNS publish error: {e}")
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR)

    return order
