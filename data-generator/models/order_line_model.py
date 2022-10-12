from models.order_model import OrderModel
from models.product_model import ProductModel


class OrderLineModel:
    def __init__(self, id_value: str, customer_age: str, unit_price: float, unit_discount: float, unit_quantity: int,
                 unit_cost: float, order: OrderModel, product: ProductModel):
        self.id_value = id_value
        self.customer_age = customer_age
        self.unit_price = unit_price
        self.unit_quantity = unit_quantity
        self.unit_discount = unit_discount
        self.unit_cost = unit_cost
        self.order = order
        self.product = product


class OrderLineRowModel:
    def __init__(self, order: OrderModel, product: ProductModel):
        self.order = order
        self.product = product
