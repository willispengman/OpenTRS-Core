"""
OpenTRS-Core

Gray palette renderer.
"""

from __future__ import annotations

import numpy as np


def render_gray(
    temperature: np.ndarray,
    minimum: float,
    maximum: float,
) -> np.ndarray:
    """
    Render grayscale image from Celsius.
    """

    image = (
        (temperature - minimum)
        / (maximum - minimum)
    )

    image = np.clip(
        image,
        0.0,
        1.0,
    )

    image = (
        image * 255
    ).astype(np.uint8)

    return image