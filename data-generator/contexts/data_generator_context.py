from logging import Logger
from typing import List

from faker import Faker

import utils
from config import Config
from date_dimension import DateDimension
from models.customer_model import CustomerModel
from models.monthly_inventory_model import MonthlyInventoryModel
from models.order_line_model import OrderLineModel
from models.order_model import OrderModel
from models.product_model import ProductModel
from models.return_model import ReturnModel
from templates.customer_template import CustomerTemplate
from templates.product_template import ProductTemplate


class DataGeneratorContext:
    def __init__(self, logger: Logger, config: Config):
        self._logger = logger
        self._config = config
        self._fake = Faker(['en_US'], use_weighting=True)
        self._date_dimension = DateDimension(config.days)
        self._customers: List[CustomerModel] = []
        self._products: List[ProductModel] = []
        self._orders: List[OrderModel] = []
        self._order_lines: List[OrderLineModel] = []
        self._returns: List[ReturnModel] = []
        self._monthly_inventories: List[MonthlyInventoryModel] = []
        self._product_template_rows = ProductTemplate().read(utils.get_file_path('csvs/products.csv'))
        self._customer_template_rows = CustomerTemplate().read(utils.get_file_path('csvs/customers.csv'))
        self._merchants = self._get_merchants()

    @property
    def logger(self) -> Logger:
        return self._logger

    @property
    def config(self) -> Config:
        return self._config

    @property
    def fake(self) -> Faker:
        return self._fake

    @property
    def date_dimension(self) -> DateDimension:
        return self._date_dimension

    @property
    def customers(self) -> List[CustomerModel]:
        return self._customers

    @property
    def products(self) -> List[ProductModel]:
        return self._products

    @property
    def orders(self) -> List[OrderModel]:
        return self._orders

    @property
    def order_lines(self) -> List[OrderLineModel]:
        return self._order_lines

    @property
    def returns(self) -> List[ReturnModel]:
        return self._returns

    @property
    def monthly_inventories(self) -> List[MonthlyInventoryModel]:
        return self._monthly_inventories

    @property
    def product_template_rows(self) -> List[ProductTemplate]:
        return self._product_template_rows

    @property
    def customer_template_rows(self) -> List[CustomerTemplate]:
        return self._customer_template_rows

    @property
    def merchants(self) -> List[str]:
        return self._merchants

    def add_customer(self, customer: CustomerModel):
        self._customers.append(customer)

    def set_products(self, products: List[ProductModel]):
        self._products = products

    def set_orders(self, orders: List[OrderModel]):
        self._orders = orders

    def set_order_lines(self, order_lines: List[OrderLineModel]):
        self._order_lines = order_lines

    def set_returns(self, returns: List[ReturnModel]):
        self._returns = returns

    def set_monthly_inventories(self, monthly_inventories: List[MonthlyInventoryModel]):
        self._monthly_inventories = monthly_inventories

    def _get_merchants(self) -> List[str]:
        result = []
        for row in self._product_template_rows:
            if row.client_id not in result:
                result.append(row.client_id)
        return result
