from typing import List, Any

from exporters.exporter import Exporter


class ProductExporter(Exporter):

    def get_csv_file_name(self) -> str:
        return "product.csv"

    def get_headers(self) -> List[str]:
        return ["PRODUCT_ID", "LS__PRODUCT_ID__PRODUCT_NAME", "LS__PRODUCT_ID__PRODUCT_ID_IMAGE_WEB", "PRODUCT_BRAND",
                "PRODUCT_CATEGORY", "PRODUCT_IMAGE", "LS__PRODUCT_IMAGE__PRODUCT_IMAGE_WEB", "RATING", "WDF__CLIENT_ID",
                "PRODUCT_RATING"]

    def get_rows(self) -> List[List[Any]]:
        rows = []
        self.context.products.sort(key=lambda item: item.template.name)
        for product in self.context.products:
            rows.append([product.id_value, product.template.name, product.template.image, product.template.brand,
                         product.template.category, product.template.image, product.template.image,
                         product.template.rating, product.template.client_id, product.template.round_rating])
        return rows
