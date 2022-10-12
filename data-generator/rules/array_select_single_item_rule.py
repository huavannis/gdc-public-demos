import random
from typing import Any, List

from rules.rule import Rule


class ArraySelectSingleItemRule(Rule):
    def apply(self, array: List[Any]) -> Any:
        return random.choice(array)
