"""
OpenTRS-Core

Planck Equation

Copyright (c) 2026 Willis Peng
License: Apache-2.0
"""

from __future__ import annotations

import math

from opentrs.metadata.model import RadiometricMetadata


def raw_to_kelvin(
    raw: float,
    metadata: RadiometricMetadata,
) -> float:
    """
    Convert a raw detector value to Kelvin using the
    simplified FLIR Planck equation.

    This implementation currently ignores atmospheric
    compensation and assumes the metadata already
    contains valid Planck constants.
    """

    if metadata.possible_planck_r1 is None:
        raise ValueError("Planck R1 is missing.")

    if metadata.possible_planck_b is None:
        raise ValueError("Planck B is missing.")

    if metadata.possible_planck_f is None:
        raise ValueError("Planck F is missing.")

    if metadata.possible_planck_r2 is None:
        raise ValueError("Planck R2 is missing.")

    if metadata.possible_planck_o is None:
        raise ValueError("Planck O is missing.")

    return (
        metadata.possible_planck_b
        / math.log(
            metadata.possible_planck_r1
            / (
                metadata.possible_planck_r2
                * (
                    raw
                    + metadata.possible_planck_o
                )
            )
            + metadata.possible_planck_f
        )
    )


def raw_to_celsius(
    raw: float,
    metadata: RadiometricMetadata,
) -> float:
    """
    Convert a raw detector value to Celsius.
    """

    return raw_to_kelvin(
        raw,
        metadata,
    ) - 273.15