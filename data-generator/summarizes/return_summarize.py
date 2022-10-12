from grouper import Grouper
from models.order_model import OrderModel, OrderStatus
from summarizes.summarize import Summarize


class ReturnSummarize(Summarize):
    def summarize(self):
        self._summarize_return_processed_order_only()
        self._summarize_return_processed_order_percentage()

    def _summarize_return_processed_order_only(self):
        self.context.logger.info("Return for Processed order only")
        has_error = False
        for return_item in self.context.returns:
            if return_item.order_line.order.status != OrderStatus.PROCESSED:
                has_error = True
                self.context.logger.error(
                    f"  -> ERROR: {return_item.order_line.order.client_id} - {return_item.id_value} - {return_item.order_line.order.status}")
        if has_error is not True:
            self.context.logger.info(f"  -> OK")
        self.context.logger.info("-------------------------------------------")

    def _summarize_return_processed_order_percentage(self):
        self.context.logger.info("Return Processed order percentage")
        order_group_by_merchant = Grouper().group_array_by_field(self.context.orders, "client_id")
        returns_group_by_merchant = Grouper().group_array_by_field(self.context.returns, "order_line.order.client_id")
        for merchant in self.context.merchants:
            min_percentage = self.context.config.return_min_percentage(merchant)
            max_percentage = self.context.config.return_max_percentage(merchant)
            self.context.logger.info(f"  {merchant}: from {min_percentage}% to {max_percentage}%")
            orders_in_merchant = order_group_by_merchant.get(merchant)
            returns_in_merchant = returns_group_by_merchant.get(merchant)
            returns_group_by_order_id = Grouper().group_array_by_field(returns_in_merchant, "order_line.order.id_value")
            return_orders_len = len(returns_group_by_order_id.keys())
            orders_len = len(
                Grouper().group_array_by_field(orders_in_merchant, "status.name").get(OrderStatus.PROCESSED.name))
            return_percentage = round(return_orders_len * 100 / orders_len)
            has_error = False
            if return_percentage < min_percentage or return_percentage > max_percentage:
                has_error = True
                self.context.logger.error(f"  -> ERROR: {return_percentage}%")
            if has_error is not True:
                self.context.logger.info(
                    f"  -> OK: {return_percentage}%")
        self.context.logger.info("-------------------------------------------")

    def _group_orders_by_day_key_condition(self, order: OrderModel):
        return self.context.date_dimension.get_day_key(order.date.date_time)
