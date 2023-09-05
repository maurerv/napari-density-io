"""
This module is an example of a barebones writer plugin for napari.

It implements the Writer specification.
see: https://napari.org/stable/plugins/guides.html?#writers

Replace code below according to your needs.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Sequence, Tuple, Union

import yaml
from os.path import splitext

import numpy as np

from tme import Density

if TYPE_CHECKING:
    DataType = Union[Any, Sequence[Any]]
    FullLayerData = Tuple[DataType, dict, str]


def write_single_image(path: str, data: Any, meta: dict) -> List[str]:
    """Writes a single image layer"""

    base, _ = splitext(path)
    metadata = meta.get("metadata", {})
    Density(
        data = data,
        origin = metadata.get("origin", np.zeros(data.ndim)),
        sampling_rate = metadata.get("sampling_rate", np.ones(data.ndim))
    ).to_file(path, gzip = metadata.get("write_gzip", False))

    filter_parameters = metadata.get("filter_parameters", None)
    if filter_parameters:
        with open(f"{base}.yaml", mode = "w", encoding = "utf-8") as ofile:
            yaml.dump(filter_parameters, ofile)

    # return path to any file(s) that were successfully written
    return [path]


def write_multiple(path: str, data: List[FullLayerData]) -> List[str]:
    """Writes multiple layers of different types."""

    if isinstance(data, list):
        data, meta, *_ = data[0]

    return write_single_image(path, data, meta)
