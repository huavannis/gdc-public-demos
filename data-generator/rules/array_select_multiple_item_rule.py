import random
from typing import Any, List

from grouper import Grouper
from rules.rule import Rule


class ArraySelectMultipleItemRule(Rule):
    def apply(self, array: List[Any], number_of_items: int, allow_duplicated: bool = False,
              max_duplicated: int = 0) -> List[Any]:
        return self._random(array, number_of_items, allow_duplicated, max_duplicated)

    def _random(self, array: List[Any], number_of_items: int, allow_duplicated: bool, max_duplicated: int) -> List[Any]:
        result = self._do_random(array, number_of_items, allow_duplicated)
        # we allow duplicated and has the limited the maximum elements duplicated
        if allow_duplicated and max_duplicated > 1:
            result_group_by = Grouper().group_array(result)
            for item in result_group_by:
                if len(result_group_by.get(item)) > max_duplicated:
                    return self._random(array, number_of_items, allow_duplicated, max_duplicated)
        return result

    @staticmethod
    def _do_random(array: List[Any], number_of_items: int, allow_duplicated: bool) -> List[Any]:
        if allow_duplicated:
            return random.choices(array, k=number_of_items)
        return random.sample(array, k=number_of_items)
