#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (C) 2022 GoodData Corporation

from contexts.data_generator_context import DataGeneratorContext
from generators.monthly_inventory_generator import MonthlyInventoryGenerator
from generators.order_generator import OrderGenerator
from generators.order_line_generator import OrderLineGenerator
from generators.product_generator import ProductGenerator
from generators.return_generator import ReturnGenerator


class DataGenerator:
    @staticmethod
    def generate(context: DataGeneratorContext):
        context.logger.info("-------------------------------------------")
        context.logger.info("             DATA GENERATOR                ")
        context.logger.info("-------------------------------------------")
        ProductGenerator(context).generate()
        OrderGenerator(context).generate()
        OrderLineGenerator(context).generate()
        ReturnGenerator(context).generate()
        MonthlyInventoryGenerator(context).generate()
