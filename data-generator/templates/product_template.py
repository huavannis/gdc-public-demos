from __future__ import annotations

from typing import Any, List

from models.product_model import ProductTemplateModel
from templates.csv_template import CsvTemplate


class ProductTemplate(CsvTemplate):
    def build_row(self, row: List[Any]) -> ProductTemplateModel:
        return ProductTemplateModel(name=row[1].strip(),
                                    brand=row[3].strip(),
                                    category=row[4].strip(),
                                    image=row[5].strip(),
                                    rating=row[7].strip(),
                                    client_id=row[8].strip(),
                                    round_rating=row[9].strip())
