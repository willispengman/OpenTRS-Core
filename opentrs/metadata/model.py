"""
OpenTRS-Core

Radiometric Metadata

Copyright (c) 2026 Willis Peng
License: Apache-2.0
"""

from dataclasses import dataclass


@dataclass(slots=True)
class RadiometricMetadata:
    """
    Radiometric metadata extracted from a FLIR FFF block.

    Most fields are still under investigation and may change as
    additional FLIR cameras are analyzed.
    """

    # Confirmed / highly likely

    emissivity: float | None = None

    object_distance_m: float | None = None

    reflected_temperature_k: float | None = None

    atmospheric_temperature_k: float | None = None

    # Reverse engineering candidates

    unknown_0174: float | None = None

    unknown_017C: float | None = None

    unknown_0180: float | None = None

    possible_planck_r1: float | None = None

    possible_planck_b: float | None = None

    possible_planck_f: float | None = None