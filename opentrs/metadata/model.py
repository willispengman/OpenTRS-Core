"""
OpenTRS-Core

Radiometric Metadata Model

Copyright (c) 2026 Willis Peng
License: Apache-2.0
"""

from dataclasses import dataclass


@dataclass(slots=True)
class RadiometricMetadata:
    """
    Radiometric metadata required for temperature conversion.
    """

    emissivity: float | None = None
    object_distance_m: float | None = None
    reflected_temperature_c: float | None = None
    atmospheric_temperature_c: float | None = None
    relative_humidity: float | None = None

    planck_r1: float | None = None
    planck_r2: float | None = None
    planck_b: float | None = None
    planck_f: float | None = None
    planck_o: float | None = None