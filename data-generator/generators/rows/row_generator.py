from typing import Any, List

from contexts.data_generator_context import DataGeneratorContext


class RowGenerator:
    def __init__(self, context: DataGeneratorContext):
        self._context = context

    def generate(self) -> List[Any]:
        raise NotImplementedError

    @property
    def context(self) -> DataGeneratorContext:
        return self._context
