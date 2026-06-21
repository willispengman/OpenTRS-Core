"""
OpenTRS Frame

Copyright (c) 2026 Willis Peng
License: Apache-2.0
"""

from dataclasses import dataclass
import numpy as np


@dataclass
class TRSFrame:
    """
    One frame stored in OpenTRS reference space.
    """

    width: int
    height: int

    temperature: np.ndarray