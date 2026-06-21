"""
FFF Record

Copyright (c) 2026 Willis Peng
License: Apache-2.0
"""

from dataclasses import dataclass


@dataclass(slots=True)
class FFFRecord:
    record_type: int
    record_subtype: int
    offset: int
    size: int
    data: bytes