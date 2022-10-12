from contexts.data_generator_context import DataGeneratorContext

from summarizes.customer_summarize import CustomerSummarize
from summarizes.order_summarize import OrderSummarize
from summarizes.return_summarize import ReturnSummarize


class DataSummarize:

    @staticmethod
    def summarize(context: DataGeneratorContext):
        context.logger.info("                 SUMMARIZE                  ")
        context.logger.info("--------------------------------------------")
        CustomerSummarize(context).summarize()
        OrderSummarize(context).summarize()
        ReturnSummarize(context).summarize()
