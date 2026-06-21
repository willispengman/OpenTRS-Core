"""
OpenTRS-Core

Raw Thermal Frame

Copyright (c) 2026 Willis Peng
License: Apache-2.0
"""

from dataclasses import dataclass

import numpy as np


@dataclass(slots=True)
class RawFrame:
    """
    Raw 16-bit thermal frame decoded from JPEG-LS.

    This class stores the original sensor values before any
    radiometric conversion is applied.
    """

    width: int
    height: int
    data: np.ndarray

    @property
    def shape(self) -> tuple[int, int]:
        return self.data.shape

    @property
    def dtype(self):
        return self.data.dtype