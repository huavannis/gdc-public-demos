from typing import List, Any

from exporters.exporter import Exporter


class ReturnExporter(Exporter):

    def get_csv_file_name(self) -> str:
        return "returns.csv"

    def get_headers(self) -> List[str]:
        return ["RETURN_ID", "ORDER__ORDER_ID", "PRODUCT__PRODUCT_ID", "CUSTOMER__CUSTOMER_ID", "RETURN_UNIT_COST",
                "RETURN_UNIT_QUANTITY", "WDF__CLIENT_ID", "RETURN_UNIT_PAID_AMOUNT", "DATE", "RETURN_DATE"]

    def get_rows(self) -> List[List[Any]]:
        rows = []
        self.context.returns.sort(key=lambda item: item.date.date_time)
        for item in self.context.returns:
            rows.append([item.id_value,
                         item.order_line.order.id_value,
                         item.order_line.product.id_value,
                         item.order_line.order.customer.id_value,
                         item.unit_cost,
                         item.unit_quantity,
                         item.order_line.order.client_id,
                         item.paid_amount,
                         item.date.format_datetime(),
                         item.date.format_datetime()])
        return rows
