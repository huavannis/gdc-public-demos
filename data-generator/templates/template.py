from __future__ import annotations

from pathlib import Path
from typing import Any


class Template:
    def read(self, file_path: str | Path) -> Any:
        raise NotImplementedError
