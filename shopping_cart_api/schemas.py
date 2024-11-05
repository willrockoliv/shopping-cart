from datetime import date
from typing import Optional

from pydantic import BaseModel


class OrderSchema(BaseModel):
    uuid: Optional[str] = None
    buyer_id: int
    product_id: int
    number_of_installments: int
    total_amount: float
    purchase_date: date
