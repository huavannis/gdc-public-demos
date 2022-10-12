from __future__ import annotations

from typing import List, Any


class Writer:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def write_row(self, data: List[Any]):
        raise NotImplementedError

    def append_rows(self, data: List[Any]):
        raise NotImplementedError
