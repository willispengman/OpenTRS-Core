"""
OpenTRS-Core

Metadata Parser

Copyright (c) 2026 Willis Peng
License: Apache-2.0
"""

import struct

from opentrs.metadata.model import RadiometricMetadata


class MetadataParser:
    """
    Parser for radiometric metadata candidates.

    Current implementation is based on observed offsets from FLIR FFF/RTP blocks.
    These offsets are still under investigation.
    """

    EMISSIVITY_OFFSET = 0x0160
    OBJECT_DISTANCE_OFFSET = 0x0164

    def __init__(self, data: bytes):
        self.data = data

    def _read_float32(self, offset: int) -> float:
        return struct.unpack(
            "<f",
            self.data[offset : offset + 4],
        )[0]

    def parse(self) -> RadiometricMetadata:
        return RadiometricMetadata(
            emissivity=self._read_float32(self.EMISSIVITY_OFFSET),
            object_distance_m=self._read_float32(self.OBJECT_DISTANCE_OFFSET),
        )