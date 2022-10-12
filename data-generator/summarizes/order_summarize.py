from typing import List, Dict, Any

from grouper import Grouper
from models.order_model import OrderModel, OrderStatus
from summarizes.summarize import Summarize


class OrderSummarize(Summarize):
    def summarize(self):
        self._summarize_order_per_day()
        self._summarize_time_percentage()
        self._summarize_order_status_in_cart()
        self._summarize_order_status_canceled()

    def _summarize_order_per_day(self):
        self.context.logger.info("Order per day")
        orders_group_by_merchant = Grouper().group_array_by_field(self.context.orders, "client_id")
        for merchant in self.context.merchants:
            order_per_day_min_in_merchant = self.context.config.order_per_day_min(merchant)
            order_per_day_max_in_merchant = self.context.config.order_per_day_max(merchant)
            self.context.logger.info(
                f"  {merchant}: from {order_per_day_min_in_merchant} to {order_per_day_max_in_merchant}")
            orders_in_merchant = orders_group_by_merchant.get(merchant)
            orders_group_by_day_key = Grouper().group_array_by_field_condition(orders_in_merchant,
                                                                               self._group_orders_by_day_key_condition)
            has_error = False
            for date in self.context.date_dimension.available_date_times:
                day_key = self.context.date_dimension.get_day_key(date)
                orders_in_day = orders_group_by_day_key.get(day_key)
                orders_in_day_len = len(orders_in_day)
                if orders_in_day_len < order_per_day_min_in_merchant or orders_in_day_len > order_per_day_max_in_merchant:
                    has_error = True
                    self.context.logger.error(f"      -> ERROR: {day_key} = {orders_in_day_len}")
            if has_error is not True:
                self.context.logger.info(f"      -> All OK")
        self.context.logger.info("-------------------------------------------")

    def _summarize_time_percentage(self):
        self.context.logger.info("Order time percentage")
        orders_group_by_merchant = Grouper().group_array_by_field(self.context.orders, "client_id")
        for merchant in self.context.merchants:
            time_hour_from = self.context.config.time_hour_from(merchant)
            time_hour_to = self.context.config.time_hour_to(merchant)
            time_hour_percentage = self.context.config.time_hour_percentage(merchant)
            self.context.logger.info(
                f"  {merchant}: from {time_hour_from} to {time_hour_to} percentage {time_hour_percentage}%")
            orders_in_merchant = orders_group_by_merchant.get(merchant)
            orders_in_range = self._get_orders_in_range(orders_in_merchant, time_hour_from, time_hour_to)
            percentage = round(len(orders_in_range) * 100 / len(orders_in_merchant))
            has_error = False
            if percentage < time_hour_percentage:
                has_error = True
                self.context.logger.error(f"      -> ERROR: {percentage}%")
            if has_error is not True:
                self.context.logger.info(f"      -> OK: {percentage}%")
        self.context.logger.info("-------------------------------------------")

    def _summarize_order_status_in_cart(self):
        orders_group_by_merchant = Grouper().group_array_by_field(self.context.orders, "client_id")
        current_month_key = self.context.date_dimension.get_month_key()
        last_3_month_keys = self.context.date_dimension.get_last_n_month_keys(3)
        self._do_summarize_order_status("Order status In Cart current month", [current_month_key],
                                        orders_group_by_merchant, OrderStatus.IN_CART,
                                        self.context.config.order_status_in_cart_current_month_percentage)
        self._do_summarize_order_status("Order status In Cart last 3 months", last_3_month_keys,
                                        orders_group_by_merchant, OrderStatus.IN_CART,
                                        self.context.config.order_status_in_cart_last_3_months_percentage)
        other_month_keys = []
        for month_key in self.context.date_dimension.available_date_times_by_month:
            if month_key != current_month_key and month_key not in last_3_month_keys:
                other_month_keys.append(month_key)
        self._do_summarize_order_status("Order status In Cart other months", other_month_keys, orders_group_by_merchant,
                                        OrderStatus.IN_CART,
                                        self.context.config.order_status_in_cart_other_months_percentage)

    def _summarize_order_status_canceled(self):
        self.context.logger.info("Order status Canceled in month")
        orders_group_by_merchant = Grouper().group_array_by_field(self.context.orders, "client_id")
        for merchant in self.context.merchants:
            percentage_min = self.context.config.order_status_canceled_in_month_min_percentage(merchant)
            percentage_max = self.context.config.order_status_canceled_in_month_max_percentage(merchant)
            self.context.logger.info(f"  {merchant}: from {percentage_min}% to {percentage_max}%")
            orders_len_by_status = 0
            orders_len = 0
            orders_in_merchant = orders_group_by_merchant.get(merchant)
            orders_group_by_month_key = Grouper().group_array_by_field_condition(orders_in_merchant,
                                                                                 self._group_orders_by_month_key_condition)
            for month_key in self.context.date_dimension.available_date_times_by_month:
                orders_in_current_month = orders_group_by_month_key.get(month_key)
                orders_by_status = self._get_orders_by_status(orders_in_current_month, OrderStatus.CANCELED)
                orders_len += len(orders_in_current_month)
                orders_len_by_status += len(orders_by_status)
            order_percentage = round(orders_len_by_status * 100 / orders_len)
            has_error = False
            if order_percentage < percentage_min or order_percentage > percentage_max:
                has_error = True
                self.context.logger.error(f"      -> ERROR: {order_percentage}%")
            if has_error is not True:
                self.context.logger.info(f"      -> OK: {order_percentage}%")
        self.context.logger.info("-------------------------------------------")

    def _do_summarize_order_status(self, title: str, month_keys: List[str],
                                   orders_group_by_merchant: Dict[str, List[OrderModel]],
                                   order_status: OrderStatus, percentage_callback: Any):
        self.context.logger.info(title)
        for merchant in self.context.merchants:
            percentage = percentage_callback(merchant)
            self.context.logger.info(f"  {merchant}: {percentage}%")
            orders_len_by_status = 0
            orders_len = 0
            orders_in_merchant = orders_group_by_merchant.get(merchant)
            orders_group_by_month_key = Grouper().group_array_by_field_condition(orders_in_merchant,
                                                                                 self._group_orders_by_month_key_condition)
            for month_key in month_keys:
                orders_in_current_month = orders_group_by_month_key.get(month_key)
                orders_by_status = self._get_orders_by_status(orders_in_current_month, order_status)
                orders_len += len(orders_in_current_month)
                orders_len_by_status += len(orders_by_status)
            order_percentage = round(orders_len_by_status * 100 / orders_len)
            has_error = False
            if order_percentage < percentage:
                has_error = True
                self.context.logger.error(f"      -> ERROR: {order_percentage}%")
            if has_error is not True:
                self.context.logger.info(f"      -> OK: {order_percentage}%")
        self.context.logger.info("-------------------------------------------")

    def _group_orders_by_day_key_condition(self, order: OrderModel):
        return self.context.date_dimension.get_day_key(order.date.date_time)

    def _group_orders_by_month_key_condition(self, order: OrderModel):
        return self.context.date_dimension.get_month_key(order.date.date_time)

    @staticmethod
    def _get_orders_by_status(orders: List[OrderModel], order_status: OrderStatus) -> List[OrderModel]:
        return [order for order in orders if order.status == order_status]

    @staticmethod
    def _get_orders_in_range(orders: List[OrderModel], hour_from: int, hour_to: int) -> List[
        OrderModel]:
        result = []
        for order in orders:
            order_date = order.date.date_time
            if hour_from <= order_date.hour <= hour_to:
                result.append(order)
        return result
