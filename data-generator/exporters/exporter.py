import os
from typing import List, Any

import numpy

from contexts.data_generator_context import DataGeneratorContext
from writers.csv_writer import CsvWriter


class Exporter:
    def __init__(self, context: DataGeneratorContext):
        self._context = context
        output = os.path.join(os.getcwd(), "output")
        csv_file_path = os.path.join(output, self.get_csv_file_name())
        self._writer = CsvWriter(file_path=csv_file_path)

    def export(self):
        self._context.logger.info(f" Exporting {self.get_csv_file_name()}")
        self._writer.write_row(self.get_headers())
        rows = self.get_rows()
        self._context.logger.info(f" Total records: {len(rows)}")
        row_chunks = numpy.array_split(rows, 50)
        for row_chunk in row_chunks:
            self._writer.append_rows(row_chunk)
        self._context.logger.info(" Done")
        self._context.logger.info("-------------------------------------------")

    @property
    def context(self):
        return self._context

    def get_csv_file_name(self) -> str:
        raise NotImplementedError

    def get_headers(self) -> List[str]:
        raise NotImplementedError

    def get_rows(self) -> List[List[Any]]:
        raise NotImplementedError
