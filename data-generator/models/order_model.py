import enum
from datetime import datetime
from typing import List

from models.custom_datetime_model import CustomDateTimeModel
from models.customer_model import CustomerModel
from models.product_model import ProductModel


class OrderStatus(enum.Enum):
    IN_CART = "In Cart"
    PROCESSED = "Processed"
    CANCELED = "Canceled"


class OrderModel:
    def __init__(self, id_value: str, date: CustomDateTimeModel, client_id: str, status: OrderStatus,
                 customer: CustomerModel, products: List[ProductModel]):
        self.id_value = id_value
        self.date = date
        self.client_id = client_id
        self.status = status
        self.customer = customer
        self.products = products


class OrderRowModel:
    def __init__(self, date: datetime, client_id: str, customer: CustomerModel, products: List[ProductModel]):
        self.date = date
        self.client_id = client_id
        self.customer = customer
        self.products = products
