from contexts.data_generator_context import DataGeneratorContext
from generators.columns.column_generator import ColumnGenerator
from models.custom_datetime_model import CustomDateTimeModel
from models.monthly_inventory_model import MonthlyInventoryRowModel, MonthlyInventoryModel
from rules.id_rule import IdRule


class MonthlyInventoryColumnGenerator(ColumnGenerator):
    def __init__(self, context: DataGeneratorContext):
        super().__init__(context)
        self._id_rule = IdRule()

    def generate(self, row: MonthlyInventoryRowModel) -> MonthlyInventoryModel:
        id_value = self._id_rule.apply(prefix="M")
        eom = row.bom - row.order_quantity_in_month
        return MonthlyInventoryModel(id_value=id_value,
                                     bom=row.bom,
                                     eom=eom,
                                     inventory_month=CustomDateTimeModel(row.inventory_month),
                                     product=row.product)
