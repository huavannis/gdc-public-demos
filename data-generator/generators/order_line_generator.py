from typing import List, NoReturn

from contexts.data_generator_context import DataGeneratorContext
from generators.columns.order_line_column_generator import OrderLineColumnGenerator
from generators.generator import Generator
from generators.rows.order_line_row_generator import OrderLineRowGenerator
from models.order_line_model import OrderLineModel


class OrderLineGenerator(Generator):
    def __init__(self, context: DataGeneratorContext):
        super().__init__("order_lines", OrderLineRowGenerator(context), OrderLineColumnGenerator(context), context)

    def store_data(self, data: List[OrderLineModel]) -> NoReturn:
        self.context.set_order_lines(data)
