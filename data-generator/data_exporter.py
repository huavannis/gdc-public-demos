from contexts.data_generator_context import DataGeneratorContext
from exporters.customer_exporter import CustomerExporter
from exporters.monthly_inventory_exporter import MonthlyInventoryExporter
from exporters.order_exporter import OrderExporter
from exporters.order_line_exporter import OrderLineExporter
from exporters.product_exporter import ProductExporter
from exporters.return_exporter import ReturnExporter


class DataExporter:

    @staticmethod
    def export(context: DataGeneratorContext):
        context.logger.info("                 EXPORTER                  ")
        context.logger.info("-------------------------------------------")
        ProductExporter(context).export()
        CustomerExporter(context).export()
        OrderExporter(context).export()
        OrderLineExporter(context).export()
        ReturnExporter(context).export()
        MonthlyInventoryExporter(context).export()
