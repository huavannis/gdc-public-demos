from datetime import datetime

from contexts.data_generator_context import DataGeneratorContext
from generators.columns.column_generator import ColumnGenerator
from models.order_line_model import OrderLineRowModel, OrderLineModel
from rules.id_rule import IdRule
from rules.range_rule import RangeRule
from rules.range_uniform_rule import RangeUniformRule
from rules.sub_range_percentage_rule import SubRangePercentageRule


class OrderLineColumnGenerator(ColumnGenerator):
    def __init__(self, context: DataGeneratorContext):
        super().__init__(context)
        self._id_rule = IdRule()
        self._range_rule = RangeRule()
        self._range_uniform_rule = RangeUniformRule()
        self._discount_rule = SubRangePercentageRule(0, 1)

    def generate(self, row: OrderLineRowModel) -> OrderLineModel:
        id_value = self._id_rule.apply(prefix="L")
        unit_price = self._range_uniform_rule.apply(2, 1000, 2)
        unit_cost = self._range_uniform_rule.apply(2, unit_price, 2)
        unit_quantity = self._range_rule.apply(1, 10)
        unit_discount = self._discount_rule.apply(0, 0, 10)
        if unit_discount != 0:
            unit_discount = self._range_uniform_rule.apply(1, round(unit_price * 50 / 100), 2)
        customer_age = self.__calculate_customer_age(row.order.date.date_time,
                                                     row.order.customer.created_date.date_time)
        return OrderLineModel(id_value=id_value,
                              customer_age=customer_age,
                              unit_price=unit_price,
                              unit_quantity=unit_quantity,
                              unit_discount=unit_discount,
                              unit_cost=unit_cost,
                              order=row.order,
                              product=row.product)

    @staticmethod
    def __calculate_customer_age(date_time: datetime, cust_created_date: datetime):
        range_date_time = date_time - cust_created_date
        if range_date_time.days <= 90:
            return "1-3M"
        elif range_date_time.days <= 240:
            return "4-6M"
        return "7M+"
