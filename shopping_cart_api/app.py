import logging
import uuid
from datetime import date
from http import HTTPStatus
from typing import Optional

from fastapi import FastAPI
from mangum import Mangum
from pydantic import BaseModel

app = FastAPI()
handler = Mangum(app)


class OrderSchema(BaseModel):
    uuid: Optional[str] = None
    buyer_id: int
    product_id: int
    number_of_installments: int
    total_amount: float
    purchase_date: date


@app.get("/")
async def hello_world():
    return {"message": "Hi! 👋"}


@app.post("/order/", status_code=HTTPStatus.CREATED, response_model=OrderSchema)
async def create_order(order: OrderSchema):
    logging.info(f"send to sns topic: {order}")

    if not order.uuid:
        order.uuid = uuid.uuid4()

    return order
