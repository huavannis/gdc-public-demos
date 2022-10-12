from typing import List, Any

from contexts.data_generator_context import DataGeneratorContext
from generators.columns.column_generator import ColumnGenerator
from generators.rows.row_generator import RowGenerator


class Generator:
    def __init__(self, name: str, row_generator: RowGenerator, column_generator: ColumnGenerator,
                 context: DataGeneratorContext):
        self._name = name
        self._row_generator = row_generator
        self._column_generator = column_generator
        self._context = context

    def generate(self):
        self._context.logger.info(f" Generating {self._name}")
        rows = self._row_generator.generate()
        total_records = len(rows)
        self._context.logger.info(f" Total records: {total_records}")
        result = []
        i = 0
        for row in rows:
            result.append(self._column_generator.generate(row))
            i += 1
            if i % 1000 == 0:
                self._context.logger.info(f" progress: {i}/{total_records}")
        if i > 1000:
            self._context.logger.info(f" progress: {i}/{total_records}")
        self.store_data(result)
        self._context.logger.info(" Done")
        self._context.logger.info("-------------------------------------------")

    def store_data(self, data: List[Any]):
        raise NotImplementedError

    @property
    def context(self) -> DataGeneratorContext:
        return self._context
