from typing import List, NoReturn

from contexts.data_generator_context import DataGeneratorContext
from generators.columns.order_column_generator import OrderColumnGenerator
from generators.generator import Generator
from generators.rows.order_row_generator import OrderRowGenerator
from models.order_model import OrderModel


class OrderGenerator(Generator):
    def __init__(self, context: DataGeneratorContext):
        super().__init__("order", OrderRowGenerator(context), OrderColumnGenerator(context), context)

    def store_data(self, data: List[OrderModel]) -> NoReturn:
        self.context.set_orders(data)
