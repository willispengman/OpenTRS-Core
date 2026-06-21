"""
OpenTRS-Core

Planck Equation

Copyright (c) 2026 Willis Peng
License: Apache-2.0
"""

from opentrs.metadata.model import RadiometricMetadata


def raw_to_temperature(
    raw: float,
    metadata: RadiometricMetadata,
) -> float:
    """
    Convert one raw sensor value into temperature.

    This function will implement the FLIR radiometric equation.
    """

    raise NotImplementedError(
        "Planck conversion has not been implemented yet."
    )