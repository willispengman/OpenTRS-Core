"""
OpenTRS-Core

Planck Equation

Copyright (c) 2026 Willis Peng
License: Apache-2.0
"""

from __future__ import annotations

import math

import numpy as np

from opentrs.metadata.model import RadiometricMetadata


def _require(value: float | None, name: str) -> float:
    if value is None:
        raise ValueError(f"{name} is missing.")

    return value


def raw_to_kelvin(
    raw: float,
    metadata: RadiometricMetadata,
) -> float:
    r1 = _require(metadata.possible_planck_r1, "Planck R1")
    r2 = _require(metadata.possible_planck_r2, "Planck R2")
    b = _require(metadata.possible_planck_b, "Planck B")
    f = _require(metadata.possible_planck_f, "Planck F")
    o = _require(metadata.possible_planck_o, "Planck O")

    return b / math.log(
        r1 / (r2 * (raw + o)) + f
    )


def raw_to_celsius(
    raw: float,
    metadata: RadiometricMetadata,
) -> float:
    return raw_to_kelvin(raw, metadata) - 273.15


def raw_array_to_kelvin(
    raw: np.ndarray,
    metadata: RadiometricMetadata,
) -> np.ndarray:
    r1 = _require(metadata.possible_planck_r1, "Planck R1")
    r2 = _require(metadata.possible_planck_r2, "Planck R2")
    b = _require(metadata.possible_planck_b, "Planck B")
    f = _require(metadata.possible_planck_f, "Planck F")
    o = _require(metadata.possible_planck_o, "Planck O")

    raw_float = raw.astype(np.float64)

    return b / np.log(
        r1 / (r2 * (raw_float + o)) + f
    )


def raw_array_to_celsius(
    raw: np.ndarray,
    metadata: RadiometricMetadata,
) -> np.ndarray:
    return raw_array_to_kelvin(raw, metadata) - 273.15