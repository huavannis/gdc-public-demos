from typing import List, Any

from exporters.exporter import Exporter


class CustomerExporter(Exporter):

    def get_csv_file_name(self) -> str:
        return "customer.csv"

    def get_headers(self) -> List[str]:
        return ["CUSTOMER_ID", "LS__CUSTOMER_ID__CUSTOMER_NAME", "CUSTOMER_CITY", "LS__CUSTOMER_CITY__CITY_PUSHPIN",
                "CUSTOMER_COUNTRY", "CUSTOMER_EMAIL", "CUSTOMER_STATE", "CUSTOMER_CREATED_DATE", "WDF__CLIENT_ID"]

    def get_rows(self) -> List[List[Any]]:
        rows = []
        self.context.customers.sort(key=lambda item: item.created_date.date_time)
        for customer in self.context.customers:
            rows.append(
                [customer.id_value, customer.template.name, customer.template.city, customer.template.city_pushpin,
                 customer.template.country, customer.template.email, customer.template.state,
                 customer.created_date.format_date(), customer.client_id])
        return rows
