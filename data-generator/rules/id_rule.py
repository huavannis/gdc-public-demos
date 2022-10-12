import random
import string
from typing import List

from rules.rule import Rule


class IdRule(Rule):
    def __init__(self):
        self._ids: List[str] = []

    def apply(self, prefix: str = None, length: int = 8) -> str:
        id_value = self._do_generate(prefix, length)
        if id_value in self._ids:
            return self.apply()
        return id_value

    @staticmethod
    def _do_generate(prefix: str, length: int) -> str:
        id_value = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
        if prefix:
            return f'{prefix}-{id_value}'
        return id_value
