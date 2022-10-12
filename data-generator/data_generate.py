#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (C) 2022 GoodData Corporation

from config import Config
from contexts.data_generator_context import DataGeneratorContext
from data_exporter import DataExporter
from data_generator import DataGenerator
from data_summarize import DataSummarize
from logger import get_logger


class DataGenerate:

    @staticmethod
    def main():
        logger = get_logger(DataGenerator.__name__)
        config = Config("config/config.yaml")
        context = DataGeneratorContext(logger=logger, config=config)
        DataGenerator.generate(context)
        DataExporter.export(context)
        DataSummarize.summarize(context)


if __name__ == "__main__":
    DataGenerate.main()
