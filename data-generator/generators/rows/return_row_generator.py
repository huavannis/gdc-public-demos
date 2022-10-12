from typing import List, Dict

from contexts.data_generator_context import DataGeneratorContext
from generators.rows.row_generator import RowGenerator
from grouper import Grouper
from models.order_line_model import OrderLineModel
from models.order_model import OrderStatus, OrderModel
from models.return_model import ReturnRowModel
from rules.array_select_multiple_item_rule import ArraySelectMultipleItemRule
from rules.range_rule import RangeRule


class ReturnRowGenerator(RowGenerator):
    def __init__(self, context: DataGeneratorContext):
        super().__init__(context)
        self._range_rule = RangeRule()
        self._array_select_multiple_item_rule = ArraySelectMultipleItemRule()

    def generate(self) -> List[ReturnRowModel]:
        result = []
        orders_group_by_merchant = Grouper().group_array_by_field(self.context.orders, "client_id")
        order_lines_group_by_order_id = Grouper().group_array_by_field(self.context.order_lines, "order.id_value")
        for merchant in self.context.merchants:
            return_orders = self._get_return_orders(orders_group_by_merchant, merchant)
            for order in return_orders:
                order_lines = order_lines_group_by_order_id.get(order.id_value)
                # return some order lines in an order, not all order lines in an order
                number_of_return_order_lines = self._range_rule.apply(1, len(order_lines))
                return_order_lines = self._array_select_multiple_item_rule.apply(order_lines,
                                                                                 number_of_return_order_lines)
                for return_order_line in return_order_lines:
                    result.append(self.__build_row(return_order_line))
        return result

    def __build_row(self, order_line: OrderLineModel) -> ReturnRowModel:
        # return order line in range 1-10 days after order
        return_period_days = self._range_rule.apply(1, 10)
        date = self.context.date_dimension.plus_n_days(date_time=order_line.order.date.date_time,
                                                       days=return_period_days)
        return ReturnRowModel(order_line=order_line, date=date)

    def _get_return_orders(self, orders_group_by_merchant: Dict[str, List[OrderModel]], merchant) -> List[
        OrderLineModel]:
        orders_in_merchant = orders_group_by_merchant.get(merchant)
        processed_orders = Grouper().group_array_by_field(orders_in_merchant, "status.name").get(
            OrderStatus.PROCESSED.name)
        percentage = self._range_rule.apply(self.context.config.return_min_percentage(merchant),
                                            self.context.config.return_max_percentage(merchant))
        number_of_return_orders = round(percentage * len(processed_orders) / 100)
        return self._array_select_multiple_item_rule.apply(processed_orders, number_of_return_orders)
