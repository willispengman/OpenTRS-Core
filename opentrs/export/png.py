"""
OpenTRS-Core

PNG Export

Copyright (c) 2026 Willis Peng
License: Apache-2.0
"""

from pathlib import Path

import imageio.v3 as iio
import numpy as np


def normalize_to_uint8(
    image: np.ndarray,
) -> np.ndarray:
    image = image.astype(np.float32)

    minimum = image.min()
    maximum = image.max()

    if maximum == minimum:
        return np.zeros_like(
            image,
            dtype=np.uint8,
        )

    image = (
        (image - minimum)
        / (maximum - minimum)
        * 255
    )

    return image.astype(np.uint8)


def save_png(
    image: np.ndarray,
    filename: str | Path,
) -> None:

    filename = Path(filename)
    filename.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    iio.imwrite(
        filename,
        image,
    )