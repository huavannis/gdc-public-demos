from __future__ import annotations

import csv
from pathlib import Path
from typing import Any, List

from templates.template import Template


class CsvTemplate(Template):
    def read(self, file_path: str | Path) -> List[Any]:
        with open(file_path) as file:
            csvreader = csv.reader(file)
            next(csvreader)
            return [self.build_row(row) for row in csvreader]

    def build_row(self, row: List[Any]) -> Any:
        raise NotImplementedError
