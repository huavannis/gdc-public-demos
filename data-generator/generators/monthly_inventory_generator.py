from typing import List, NoReturn

from contexts.data_generator_context import DataGeneratorContext
from generators.columns.monthly_inventory_column_generator import MonthlyInventoryColumnGenerator
from generators.generator import Generator
from generators.rows.monthly_inventory_row_generator import MonthlyInventoryRowGenerator
from models.monthly_inventory_model import MonthlyInventoryModel


class MonthlyInventoryGenerator(Generator):
    def __init__(self, context: DataGeneratorContext):
        super().__init__("monthlyinventory", MonthlyInventoryRowGenerator(context),
                         MonthlyInventoryColumnGenerator(context), context)

    def store_data(self, data: List[MonthlyInventoryModel]) -> NoReturn:
        self.context.set_monthly_inventories(data)
