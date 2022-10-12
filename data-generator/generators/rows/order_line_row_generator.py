from typing import List

from generators.rows.row_generator import RowGenerator
from models.order_line_model import OrderLineRowModel


class OrderLineRowGenerator(RowGenerator):
    def generate(self) -> List[OrderLineRowModel]:
        result = []
        for order in self.context.orders:
            for product in order.products:
                result.append(OrderLineRowModel(order=order, product=product))
        return result
