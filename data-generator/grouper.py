from itertools import groupby
from typing import List, Any, Dict


class Grouper:
    @staticmethod
    def group_array(array: List[Any]) -> Dict[Any, List[Any]]:
        array.sort()
        return {key: list(value) for key, value in groupby(array, key=lambda item: item)}

    @staticmethod
    def group_array_by_field_condition(array: List[Any], callback: Any = None) -> Dict[Any, List[Any]]:
        array.sort(key=lambda item: item if callback is None else callback(item))
        return {key: list(value) for key, value in
                groupby(array, key=lambda item: item if callback is None else callback(item))}

    def group_array_by_field(self, array: List[Any], field: str) -> Dict[Any, List[Any]]:
        array.sort(key=lambda item: self._get_group_by_condition(item, field))
        return {key: list(value) for key, value in
                groupby(array, key=lambda item: self._get_group_by_condition(item, field))}

    def _get_group_by_condition(self, item: Any, field: str):
        if "." not in field:
            return getattr(item, field)
        fields = field.split(".")
        for f in fields:
            return self._get_group_by_condition(getattr(item, f), field[(len(f) + 1):])
