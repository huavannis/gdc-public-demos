from __future__ import annotations

from typing import Any, List

from models.customer_model import CustomerTemplateModel
from templates.csv_template import CsvTemplate


class CustomerTemplate(CsvTemplate):
    def build_row(self, row: List[Any]) -> CustomerTemplateModel:
        return CustomerTemplateModel(name=row[1].strip(),
                                     email=row[5].strip(),
                                     city=row[2].strip(),
                                     city_pushpin=row[3].strip(),
                                     country=row[4].strip(),
                                     state=row[6].strip())
