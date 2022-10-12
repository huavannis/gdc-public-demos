from typing import List

from contexts.data_generator_context import DataGeneratorContext
from generators.rows.row_generator import RowGenerator
from grouper import Grouper
from models.monthly_inventory_model import MonthlyInventoryRowModel
from models.order_line_model import OrderLineModel
from models.product_model import ProductModel
from rules.range_rule import RangeRule


class MonthlyInventoryRowGenerator(RowGenerator):
    def __init__(self, context: DataGeneratorContext):
        super().__init__(context)
        self._range_rule = RangeRule()

    def generate(self) -> List[MonthlyInventoryRowModel]:
        result = []
        order_lines_group_by_product_id = Grouper().group_array_by_field(self.context.order_lines, "product.id_value")
        for product in self.context.products:
            order_lines = order_lines_group_by_product_id.get(product.id_value)
            order_quantity = self._get_order_line_quantity(order_lines)
            bom = self._range_rule.apply(order_quantity, order_quantity + 1000)
            order_lines_group_by_month_key = Grouper().group_array_by_field_condition(order_lines,
                                                                                      self._group_order_line_by_month_key_condition)
            for month_key in self.context.date_dimension.available_date_times_by_month:
                order_lines = order_lines_group_by_month_key.get(month_key)
                order_quantity_in_month = self._get_order_line_quantity(order_lines)
                result.append(self.__build_row(bom, order_quantity_in_month, month_key, product))
                bom -= order_quantity_in_month

        return result

    def __build_row(self, bom: int, order_quantity_in_month: int, month_key: str,
                    product: ProductModel) -> MonthlyInventoryRowModel:
        return MonthlyInventoryRowModel(bom=bom,
                                        order_quantity_in_month=order_quantity_in_month,
                                        inventory_month=self.context.date_dimension.parse_month_key(month_key),
                                        product=product)

    def _group_order_line_by_month_key_condition(self, order_line: OrderLineModel) -> str:
        return self.context.date_dimension.get_month_key(order_line.order.date.date_time)

    @staticmethod
    def _get_order_line_quantity(order_lines: List[OrderLineModel]) -> int:
        quantity = 0
        if order_lines is not None:
            for order_line in order_lines:
                quantity += order_line.unit_quantity
        return quantity
