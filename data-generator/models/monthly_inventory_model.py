from datetime import datetime

from models.custom_datetime_model import CustomDateTimeModel
from models.product_model import ProductModel


class MonthlyInventoryModel:
    def __init__(self, id_value: str, bom: int, eom: int, inventory_month: CustomDateTimeModel, product: ProductModel):
        self.id_value = id_value
        self.bom = bom
        self.eom = eom
        self.inventory_month = inventory_month
        self.product = product


class MonthlyInventoryRowModel:
    def __init__(self, bom: int, order_quantity_in_month: int, inventory_month: datetime, product: ProductModel):
        self.bom = bom
        self.order_quantity_in_month = order_quantity_in_month
        self.inventory_month = inventory_month
        self.product = product
