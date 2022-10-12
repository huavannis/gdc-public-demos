from contexts.data_generator_context import DataGeneratorContext
from generators.columns.column_generator import ColumnGenerator
from models.custom_datetime_model import CustomDateTimeModel
from models.return_model import ReturnRowModel, ReturnModel
from rules.id_rule import IdRule
from rules.time_percentage_rule import TimePercentageRule


class ReturnColumnGenerator(ColumnGenerator):
    def __init__(self, context: DataGeneratorContext):
        super().__init__(context)
        self._id_rule = IdRule()
        self._time_percentage_rule = TimePercentageRule()

    def generate(self, row: ReturnRowModel) -> ReturnModel:
        return_id = self._id_rule.apply(prefix="R")
        merchant = row.order_line.order.client_id
        date_time = self._time_percentage_rule.apply(row.date,
                                                     self.context.config.time_hour_from(merchant),
                                                     self.context.config.time_hour_to(merchant),
                                                     self.context.config.time_hour_percentage(merchant))
        paid_amount = row.order_line.unit_price - row.order_line.unit_discount
        unit_quantity = row.order_line.unit_quantity
        unit_cost = row.order_line.unit_cost
        return_date = CustomDateTimeModel(date_time)
        return ReturnModel(id_value=return_id,
                           paid_amount=paid_amount,
                           unit_quantity=unit_quantity,
                           unit_cost=unit_cost,
                           order_line=row.order_line,
                           date=return_date)
