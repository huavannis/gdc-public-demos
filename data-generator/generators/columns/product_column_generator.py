from contexts.data_generator_context import DataGeneratorContext
from generators.columns.column_generator import ColumnGenerator
from models.product_model import ProductModel, ProductTemplateModel
from rules.id_rule import IdRule


class ProductColumnGenerator(ColumnGenerator):
    def __init__(self, context: DataGeneratorContext):
        super().__init__(context)
        self._id_rule = IdRule()

    def generate(self, row: ProductTemplateModel) -> ProductModel:
        id_value = self._id_rule.apply(prefix="P")
        return ProductModel(id_value=id_value, template=row)
