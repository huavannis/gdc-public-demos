from typing import List, Any

from exporters.exporter import Exporter


class OrderExporter(Exporter):

    def get_csv_file_name(self) -> str:
        return "order.csv"

    def get_headers(self) -> List[str]:
        return ["ORDER_ID", "WDF__CLIENT_ID", "ORDER_STATUS"]

    def get_rows(self) -> List[List[Any]]:
        rows = []
        self.context.orders.sort(key=lambda item: item.date.date_time)
        for order in self.context.orders:
            rows.append([order.id_value, order.client_id, order.status.value])
        return rows
