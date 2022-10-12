from typing import Any


class Rule:
    def apply(self, *args: Any) -> Any:
        raise NotImplementedError
