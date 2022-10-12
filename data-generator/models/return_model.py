from datetime import datetime

from models.custom_datetime_model import CustomDateTimeModel
from models.order_line_model import OrderLineModel


class ReturnModel:
    def __init__(self, id_value: str, paid_amount: int, unit_quantity: int, unit_cost: int, order_line: OrderLineModel,
                 date: CustomDateTimeModel):
        self.id_value = id_value
        self.paid_amount = paid_amount
        self.unit_quantity = unit_quantity
        self.unit_cost = unit_cost
        self.order_line = order_line
        self.date = date


class ReturnRowModel:
    def __init__(self, order_line: OrderLineModel, date: datetime):
        self.order_line = order_line
        self.date = date
