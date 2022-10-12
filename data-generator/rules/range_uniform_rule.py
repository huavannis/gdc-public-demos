import random
from typing import Any

from rules.rule import Rule


class RangeUniformRule(Rule):
    def apply(self, start: int, end: int, digits: int = None) -> Any:
        val = random.uniform(start, end)
        if digits is None:
            return val
        return round(val, digits)
