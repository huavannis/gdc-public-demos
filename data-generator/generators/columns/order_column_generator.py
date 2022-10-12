from typing import Dict

from contexts.data_generator_context import DataGeneratorContext
from generators.columns.column_generator import ColumnGenerator
from models.custom_datetime_model import CustomDateTimeModel
from models.order_model import OrderRowModel, OrderModel, OrderStatus
from rules.id_rule import IdRule
from rules.range_rule import RangeRule
from rules.sub_range_percentage_rule import SubRangePercentageRule


class OrderStatusCanceledRule:
    def __init__(self, context: DataGeneratorContext, merchant: str):
        self._percentage = RangeRule().apply(context.config.order_status_canceled_in_month_min_percentage(merchant),
                                             context.config.order_status_canceled_in_month_max_percentage(merchant))
        self._rule = SubRangePercentageRule(2, 3)

    def apply(self):
        return OrderStatus.CANCELED if self._rule.apply(3, 3, self._percentage) == 3 else OrderStatus.PROCESSED

    def increase_total(self):
        self._rule.increase_total()


class OrderStatusRule:
    def __init__(self, context: DataGeneratorContext, merchant: str,
                 canceled_rule_map: Dict[str, OrderStatusCanceledRule]):
        self._current_month_percentage = context.config.order_status_in_cart_current_month_percentage(merchant)
        self._last_3_months_percentage = context.config.order_status_in_cart_last_3_months_percentage(merchant)
        self._other_months_percentage = context.config.order_status_in_cart_other_months_percentage(merchant)
        self._current_month_rule = SubRangePercentageRule(1, 3)
        self._last_3_months_rule = SubRangePercentageRule(1, 3)
        self._other_months_rule = SubRangePercentageRule(1, 3)
        self._canceled_rule_map = canceled_rule_map

    def apply_current_month_rule(self, month_key: str):
        return self._apply_rule(month_key, self._current_month_rule, self._current_month_percentage)

    def apply_last_3_months_rule(self, month_key: str):
        return self._apply_rule(month_key, self._last_3_months_rule, self._last_3_months_percentage)

    def apply_other_months_rule(self, month_key: str):
        return self._apply_rule(month_key, self._other_months_rule, self._other_months_percentage)

    def _apply_rule(self, month_key: str, rule: SubRangePercentageRule, percentage: int):
        status_index = rule.apply(1, 1, percentage)
        canceled_rule = self._canceled_rule_map[month_key]
        if status_index == 1:
            canceled_rule.increase_total()
            return OrderStatus.IN_CART
        return canceled_rule.apply()


class OrderColumnGenerator(ColumnGenerator):
    def __init__(self, context: DataGeneratorContext):
        super().__init__(context)
        self._id_rule = IdRule()
        self._range_rule = RangeRule()
        self._current_month_key = context.date_dimension.get_month_key()
        self._last_3_month_keys = context.date_dimension.get_last_n_month_keys(3)
        self._order_status_rule_map = self._build_order_status_rule_map()

    def generate(self, row: OrderRowModel) -> OrderModel:
        id_value = self._id_rule.apply(prefix="O")
        status = self._get_order_status(row)
        return OrderModel(id_value=id_value,
                          date=CustomDateTimeModel(row.date),
                          client_id=row.client_id,
                          status=status,
                          customer=row.customer,
                          products=row.products)

    def _get_order_status(self, row: OrderRowModel) -> OrderStatus:
        # 1: In Cart
        # 2: Processed
        # 3: Canceled
        merchant = row.client_id
        order_status_rule = self._order_status_rule_map.get(merchant)
        order_date_month_key = self.context.date_dimension.get_month_key(row.date)
        if order_date_month_key == self._current_month_key:
            return order_status_rule.apply_current_month_rule(order_date_month_key)
        elif order_date_month_key in self._last_3_month_keys:
            return order_status_rule.apply_last_3_months_rule(order_date_month_key)
        else:
            return order_status_rule.apply_other_months_rule(order_date_month_key)

    def _build_order_status_rule_map(self) -> Dict[str, OrderStatusRule]:
        result = {}
        for merchant in self.context.merchants:
            result[merchant] = self._build_order_status_rule(merchant)
        return result

    def _build_order_status_rule(self, merchant) -> OrderStatusRule:
        canceled_status_rule_map = self._build_order_canceled_status_rule_map(merchant)
        return OrderStatusRule(self.context, merchant, canceled_status_rule_map)

    def _build_order_canceled_status_rule_map(self, merchant) -> Dict[str, OrderStatusCanceledRule]:
        result = {}
        for month_key in self.context.date_dimension.available_date_times_by_month:
            result[month_key] = OrderStatusCanceledRule(self.context, merchant)
        return result
