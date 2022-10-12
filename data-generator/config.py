from pathlib import Path
from typing import Dict, Any

import utils
from file_locator import FileLocator


class Config:
    def __init__(self, file_path: str):
        self._config_file = self._get_config_path(file_path)
        self._config = utils.read_config_from_file(self._config_file)
        self._cache = {}

    @staticmethod
    def _get_config_path(file_path: str):
        file_locator = FileLocator.for_config(Path(__file__).parent)
        return file_locator.locate(file_path)

    def _get_value_with_check_mandatory(self, config: Dict[str, Any], key: str) -> Any:
        if "." not in key:
            utils.check_mandatory_key(config, key, self._config_file)
            return config[key]
        keys = key.split(".")
        for k in keys:
            return self._get_value_with_check_mandatory(config[k], key[(len(k) + 1):])

    @staticmethod
    def _build_cache_key(key: str, merchant: str = None, sub_key: str = None):
        if key is not None and merchant is not None and sub_key is not None:
            return f"{key}-{merchant}-{sub_key}"
        elif key is not None and merchant is not None:
            return f"{key}-{merchant}"
        elif key is not None and sub_key is not None:
            return f"{key}-{sub_key}"
        else:
            return key

    def _get_config_value(self, key: str, merchant: str = None, sub_key: str = None):
        # cache_key = self._build_cache_key(key, merchant, sub_key)
        # if cache_key in self._cache:
        #     return self._cache[cache_key]
        config_value = self._get_value_with_check_mandatory(self._config, key)
        if merchant is not None and merchant in config_value:
            config_value = config_value[merchant]
        if sub_key is not None:
            config_value = self._get_value_with_check_mandatory(config_value, sub_key)
        # self._cache[cache_key] = config_value
        return config_value

    @property
    def days(self) -> int:
        return self._get_config_value("days")

    def time_hour_from(self, merchant: str) -> int:
        return self._get_config_value("timePercentage.hour", merchant, "from")

    def time_hour_to(self, merchant: str) -> int:
        return self._get_config_value("timePercentage.hour", merchant, "to")

    def time_hour_percentage(self, merchant: str) -> int:
        return self._get_config_value("timePercentage.hour", merchant, "percentage")

    def new_customer_in_month(self, merchant: str) -> int:
        return self._get_config_value("newCustomerInMonth", merchant, None)

    def order_per_day_min(self, merchant: str) -> int:
        return self._get_config_value("orderPerDay", merchant, "min")

    def order_per_day_max(self, merchant: str) -> int:
        return self._get_config_value("orderPerDay", merchant, "max")

    def order_status_in_cart_current_month_percentage(self, merchant: str) -> int:
        return self._get_config_value("orderStatusPercentage.inCart", merchant, "currentMonth")

    def order_status_in_cart_last_3_months_percentage(self, merchant: str) -> int:
        return self._get_config_value("orderStatusPercentage.inCart", merchant, "last3Months")

    def order_status_in_cart_other_months_percentage(self, merchant: str) -> int:
        return self._get_config_value("orderStatusPercentage.inCart", merchant, "otherMonths")

    def order_status_canceled_in_month_min_percentage(self, merchant: str) -> int:
        return self._get_config_value("orderStatusPercentage.canceled", merchant, "min")

    def order_status_canceled_in_month_max_percentage(self, merchant: str) -> int:
        return self._get_config_value("orderStatusPercentage.canceled", merchant, "max")

    def return_min_percentage(self, merchant: str) -> int:
        return self._get_config_value("returnPercentage", merchant, "min")

    def return_max_percentage(self, merchant: str) -> int:
        return self._get_config_value("returnPercentage", merchant, "max")
