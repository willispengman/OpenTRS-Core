"""
OpenTRS Radiometric Metadata

Copyright (c) 2026 Willis Peng
License: Apache-2.0
"""

from dataclasses import dataclass


@dataclass
class RadiometricMetadata:
    """
    Metadata required for radiometric temperature conversion.
    """

    emissivity: float

    reflected_temperature: float

    atmospheric_temperature: float

    distance: float

    humidity: float

    planck_r1: float

    planck_r2: float

    planck_b: float

    planck_f: float

    planck_o: float