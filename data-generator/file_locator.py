# -*- coding: utf-8 -*-
# (C) 2022 GoodData Corporation
from __future__ import annotations

from glob import glob
from pathlib import Path
from typing import Generator


class FileLocator:
    def __init__(self, location_roots: list[Path]) -> None:
        self._location_roots = location_roots

    @classmethod
    def for_config(cls, configs_default: Path) -> FileLocator:
        locations = [Path.cwd(), configs_default.resolve()]
        return cls(locations)

    def locate(self, relative_path: str) -> Path:
        for root in self._location_roots:
            full_path = root / relative_path
            if full_path.exists():
                return full_path

        roots_as_str = ",".join([str(root) for root in self._location_roots])
        raise ValueError(f"{relative_path} cannot be found at locations [{roots_as_str}]")

    def glob_locate(self, relative_pattern: str) -> Generator[Path, None, None]:
        visited_file_names = set()
        for root in self._location_roots:
            files_glob = glob(f"{str(root)}/{relative_pattern}")
            for file in files_glob:
                file_path = Path(file)
                if file_path.name not in visited_file_names:
                    visited_file_names.add(file_path.name)
                    yield file_path
