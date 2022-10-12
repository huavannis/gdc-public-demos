from typing import List

from contexts.data_generator_context import DataGeneratorContext
from generators.columns.product_column_generator import ProductColumnGenerator
from generators.generator import Generator
from generators.rows.product_row_generator import ProductRowGenerator
from models.product_model import ProductModel


class ProductGenerator(Generator):
    def __init__(self, context: DataGeneratorContext):
        super().__init__("product", ProductRowGenerator(context), ProductColumnGenerator(context), context)

    def store_data(self, data: List[ProductModel]):
        self.context.set_products(data)
