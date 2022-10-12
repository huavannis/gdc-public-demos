from __future__ import annotations

from datetime import datetime
from typing import List, Dict

from contexts.data_generator_context import DataGeneratorContext
from generators.rows.row_generator import RowGenerator
from grouper import Grouper
from models.custom_datetime_model import CustomDateTimeModel
from models.customer_model import CustomerModel
from models.order_model import OrderRowModel
from models.product_model import ProductModel
from rules.array_select_multiple_item_rule import ArraySelectMultipleItemRule
from rules.array_select_single_item_rule import ArraySelectSingleItemRule
from rules.id_rule import IdRule
from rules.range_rule import RangeRule
from rules.time_percentage_rule import TimePercentageRule


class OrderRowGenerator(RowGenerator):
    def __init__(self, context: DataGeneratorContext):
        super().__init__(context)
        self._id_rule = IdRule()
        self._range_rule = RangeRule()
        self._time_percentage_rule_map = self._build_time_percentage_rule_map()
        self._array_select_single_item_rule = ArraySelectSingleItemRule()
        self._array_select_multiple_item_rule = ArraySelectMultipleItemRule()
        self._new_customers_map: Dict[str, Dict[str, List[CustomerModel]]] = {}

    def generate(self) -> List[OrderRowModel]:
        result = []
        product_group_by_merchant = Grouper().group_array_by_field(self.context.products, "template.client_id")
        for merchant in self.context.merchants:
            products = product_group_by_merchant.get(merchant)
            for date in self.context.date_dimension.available_date_times:
                month_key = self.context.date_dimension.get_month_key(date)
                is_last_day_in_month = self.context.date_dimension.is_last_day_in_month(date)
                min_order_per_day = self._get_min_order_per_day(is_last_day_in_month, month_key, merchant)
                order_per_day = self._range_rule.apply(min_order_per_day,
                                                       self.context.config.order_per_day_max(merchant))
                for i in range(order_per_day):
                    result.append(
                        self.__build_row(date, is_last_day_in_month, order_per_day - i, month_key, merchant, products))
        return result

    def __build_row(self, date: datetime, is_last_day_in_month: bool, remaining_orders: int, month_key: str,
                    merchant: str, products: List[ProductModel]) -> OrderRowModel:
        order_date = self._time_percentage_rule_map[merchant].apply(date, self.context.config.time_hour_from(merchant),
                                                                    self.context.config.time_hour_to(merchant),
                                                                    self.context.config.time_hour_percentage(merchant))
        order_customer = self._get_create_order_customer(order_date, is_last_day_in_month, remaining_orders, month_key,
                                                         merchant)
        number_of_products = self._range_rule.apply(1, min(3, len(products)))
        order_products = self._array_select_multiple_item_rule.apply(products, number_of_products)
        return OrderRowModel(date=order_date, client_id=merchant, customer=order_customer, products=order_products)

    def _get_create_order_customer(self, order_date: datetime, is_last_day_in_month: bool, remaining_orders: int,
                                   month_key: str, merchant: str) -> CustomerModel:
        if self._should_create_new_customer(is_last_day_in_month, remaining_orders, month_key, merchant):
            return self._create_new_customer(order_date, month_key, merchant)
        else:
            old_customers = self._get_old_customers(order_date, merchant)
            if len(old_customers) > 0:
                return self._array_select_single_item_rule.apply(old_customers)
            else:
                return self._create_new_customer(order_date, month_key, merchant)

    def _should_create_new_customer(self, is_last_day_in_month: bool, remaining_orders: int, month_key: str,
                                    merchant: str) -> bool:
        if is_last_day_in_month:
            remaining_new_customers = self._get_remaining_new_customers(month_key, merchant)
            if remaining_orders == remaining_new_customers:
                return True
        return self._range_rule.apply(1, 30) == 1

    def _create_new_customer(self, order_date: datetime, month_key, merchant: str) -> CustomerModel:
        id_value = self._id_rule.apply(prefix="C")
        customer_template = self._array_select_single_item_rule.apply(self.context.customer_template_rows)
        new_customer = CustomerModel(id_value=id_value,
                                     created_date=CustomDateTimeModel(order_date),
                                     client_id=merchant,
                                     template=customer_template)
        if merchant in self._new_customers_map:
            customers_in_merchant = self._new_customers_map[merchant]
            if month_key in customers_in_merchant:
                customers_in_merchant[month_key].append(new_customer)
            else:
                customers_in_merchant[month_key] = [new_customer]
        else:
            self._new_customers_map[merchant] = {month_key: [new_customer]}
        self.context.add_customer(new_customer)
        return new_customer

    def _get_old_customers(self, order_date: datetime, merchant: str) -> List[CustomerModel]:
        return [customer for customer in self.context.customers if
                customer.created_date.date_time < order_date and customer.client_id == merchant]

    def _build_time_percentage_rule_map(self) -> Dict[str, TimePercentageRule]:
        result = {}
        for merchant in self.context.merchants:
            result[merchant] = TimePercentageRule()
        return result

    def _get_min_order_per_day(self, is_last_day_in_month: bool, month_key: str, merchant: str) -> int:
        order_per_day_min = self.context.config.order_per_day_min(merchant)
        if is_last_day_in_month:
            remaining_new_customers = self._get_remaining_new_customers(month_key, merchant)
            return order_per_day_min if remaining_new_customers < order_per_day_min else remaining_new_customers
        return order_per_day_min

    def _get_remaining_new_customers(self, month_key: str, merchant: str) -> int:
        new_customer_in_month = self.context.config.new_customer_in_month(merchant)
        if merchant in self._new_customers_map:
            customers_in_merchant = self._new_customers_map[merchant]
            if month_key in customers_in_merchant:
                current_new_customers = len(customers_in_merchant[month_key])
                return 0 if current_new_customers > new_customer_in_month else new_customer_in_month - current_new_customers
        return new_customer_in_month
