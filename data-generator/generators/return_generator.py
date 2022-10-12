from typing import NoReturn, List

from contexts.data_generator_context import DataGeneratorContext
from generators.columns.return_column_generator import ReturnColumnGenerator
from generators.generator import Generator
from generators.rows.return_row_generator import ReturnRowGenerator
from models.return_model import ReturnModel


class ReturnGenerator(Generator):
    def __init__(self, context: DataGeneratorContext):
        super().__init__("returns", ReturnRowGenerator(context), ReturnColumnGenerator(context), context)

    def store_data(self, data: List[ReturnModel]) -> NoReturn:
        self.context.set_returns(data)
