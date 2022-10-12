from datetime import datetime
from typing import List

from grouper import Grouper
from models.customer_model import CustomerModel
from models.order_model import OrderModel
from summarizes.summarize import Summarize


class CustomerSummarize(Summarize):

    def summarize(self):
        self._summarize_new_customer_in_month()
        self._summarize_customer_has_order()

    def _summarize_new_customer_in_month(self):
        self.context.logger.info(f"New customers in month")
        orders_group_by_month_key = Grouper().group_array_by_field_condition(self.context.orders,
                                                                             self._group_orders_by_month_key_condition)
        customers_group_by_merchant = Grouper().group_array_by_field(self.context.customers, "client_id")
        for merchant in self.context.merchants:
            new_customers_in_month_in_merchant_config = self.context.config.new_customer_in_month(merchant)
            self.context.logger.info(f"  {merchant}: {new_customers_in_month_in_merchant_config}+")
            customers_in_merchant = customers_group_by_merchant.get(merchant)
            customers_group_by_month = Grouper().group_array_by_field_condition(customers_in_merchant,
                                                                                self._group_customers_by_month_key_condition)
            has_error = False
            for month_key in self.context.date_dimension.available_date_times_by_month:
                new_customers_in_month = []
                customers_in_month = customers_group_by_month.get(month_key)
                orders_in_month = orders_group_by_month_key.get(month_key)
                for customer in customers_in_month:
                    if self._has_order_with_date(orders_in_month, customer.created_date.date_time):
                        new_customers_in_month.append(customer)
                if len(new_customers_in_month) < new_customers_in_month_in_merchant_config:
                    has_error = True
                    self.context.logger.error(f"    -> ERROR: {month_key} = {len(new_customers_in_month)}")
            if has_error is not True:
                self.context.logger.info(f"    -> All OK")
        self.context.logger.info("-------------------------------------------")

    def _summarize_customer_has_order(self):
        self.context.logger.info("Customer has first order")
        orders_group_by_day_key = Grouper().group_array_by_field_condition(self.context.orders,
                                                                           self._group_orders_by_day_key_condition)
        has_error = False
        for customer in self.context.customers:
            customer_day_key = self.context.date_dimension.get_day_key(customer.created_date.date_time)
            orders = orders_group_by_day_key.get(customer_day_key)
            if self._has_order_with_date(orders, customer.created_date.date_time) is not True:
                has_error = True
                self.context.logger.error(f"  -> ERROR: {customer.id_value} - {customer.created_date.format_datetime()}")
        if has_error is not True:
            self.context.logger.info(f"  -> All OK")
        self.context.logger.info("-------------------------------------------")

    def _group_orders_by_month_key_condition(self, order: OrderModel):
        return self.context.date_dimension.get_month_key(order.date.date_time)

    def _group_orders_by_day_key_condition(self, order: OrderModel):
        return self.context.date_dimension.get_day_key(order.date.date_time)

    def _group_customers_by_month_key_condition(self, customer: CustomerModel):
        return self.context.date_dimension.get_month_key(customer.created_date.date_time)

    @staticmethod
    def _has_order_with_date(orders: List[OrderModel], date: datetime):
        for order in orders:
            if order.date.date_time == date:
                return True
        return False
