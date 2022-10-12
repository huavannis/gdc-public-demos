import random
from typing import Any

from rules.rule import Rule


class RangeRule(Rule):
    def apply(self, start: int, end: int) -> Any:
        return random.randint(start, end)
