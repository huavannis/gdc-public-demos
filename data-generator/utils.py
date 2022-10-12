from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from file_locator import FileLocator


def read_config_from_file(config_file: str | Path):
    with open(config_file) as fp:
        return yaml.safe_load(fp)


def check_mandatory_key(config: dict[str, Any], key: str, config_file: Path) -> None:
    if key not in config:
        raise ValueError(f"Mandatory key {key} not present in {config_file}")


def get_file_path(file_path: str):
    file_locator = FileLocator.for_config(Path(__file__).parent)
    return file_locator.locate(file_path)
