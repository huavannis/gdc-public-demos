from typing import List, Any

from exporters.exporter import Exporter


class MonthlyInventoryExporter(Exporter):

    def get_csv_file_name(self) -> str:
        return "monthlyinventory.csv"

    def get_headers(self) -> List[str]:
        return ["MONTHLY_INVENTORY_ID", "PRODUCT__PRODUCT_ID", "INVENTORY_MONTH", "MONTHLY_QUANTITY_EOM",
                "WDF__CLIENT_ID", "MONTHLY_QUANTITY_BOM", "DATE"]

    def get_rows(self) -> List[List[Any]]:
        rows = []
        self.context.monthly_inventories.sort(key=lambda item: item.inventory_month.date_time)
        for monthly_inventory in self.context.monthly_inventories:
            rows.append([monthly_inventory.id_value, monthly_inventory.product.id_value,
                         monthly_inventory.inventory_month.format_date(), monthly_inventory.eom,
                         monthly_inventory.product.template.client_id, monthly_inventory.bom,
                         monthly_inventory.inventory_month.format_datetime()])
        return rows
