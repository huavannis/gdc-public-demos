from __future__ import annotations

import csv
from pathlib import Path
from typing import List, Any

from writers.writer import Writer


class CsvWriter(Writer):
    def __init__(self, file_path: str):
        super().__init__(file_path)
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)

    def write_row(self, data: List[Any]):
        self._do_write_row('w', data)

    def append_rows(self, data: List[Any]):
        self._do_write_rows('a', data)

    def _do_write_row(self, mode: str, data: List[Any]):
        with open(self.file_path, mode, newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
            writer.writerow(data)
            csvfile.close()

    def _do_write_rows(self, mode: str, data: List[Any]):
        with open(self.file_path, mode, newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
            writer.writerows(data)
            csvfile.close()
