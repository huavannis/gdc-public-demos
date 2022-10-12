from typing import List, Any

from exporters.exporter import Exporter


class OrderLineExporter(Exporter):

    def get_csv_file_name(self) -> str:
        return "order_lines.csv"

    def get_headers(self) -> List[str]:
        return ["ORDER_LINE_ID", "ORDER__ORDER_ID", "PRODUCT__PRODUCT_ID", "CUSTOMER__CUSTOMER_ID", "ORDER_UNIT_PRICE",
                "ORDER_UNIT_QUANTITY", "WDF__CLIENT_ID", "ORDER_UNIT_DISCOUNT", "ORDER_UNIT_COST", "DATE", "ORDER_DATE",
                "CUSTOMER_AGE"]

    def get_rows(self) -> List[List[Any]]:
        rows = []
        self.context.order_lines.sort(key=lambda item: item.order.date.date_time)
        for order_line in self.context.order_lines:
            rows.append([order_line.id_value,
                         order_line.order.id_value,
                         order_line.product.id_value,
                         order_line.order.customer.id_value,
                         order_line.unit_price,
                         order_line.unit_quantity,
                         order_line.order.client_id,
                         order_line.unit_discount,
                         order_line.unit_cost,
                         order_line.order.date.format_datetime(),
                         order_line.order.date.format_datetime(),
                         order_line.customer_age])
        return rows
