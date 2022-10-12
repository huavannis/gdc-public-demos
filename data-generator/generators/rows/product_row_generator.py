from typing import List

from generators.rows.row_generator import RowGenerator
from models.product_model import ProductTemplateModel


class ProductRowGenerator(RowGenerator):
    def generate(self) -> List[ProductTemplateModel]:
        return self.context.product_template_rows
