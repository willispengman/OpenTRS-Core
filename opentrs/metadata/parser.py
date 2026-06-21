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

    Offsets are based on reverse engineering of FLIR FFF blocks.
    """

    EMISSIVITY_OFFSET = 0x0160

    OBJECT_DISTANCE_OFFSET = 0x0164

    REFLECTED_TEMP_OFFSET = 0x0168

    ATMOSPHERIC_TEMP_OFFSET = 0x016C

    UNKNOWN_0174_OFFSET = 0x0174

    UNKNOWN_017C_OFFSET = 0x017C

    UNKNOWN_0180_OFFSET = 0x0180

    POSSIBLE_PLANCK_R1_OFFSET = 0x0198

    POSSIBLE_PLANCK_B_OFFSET = 0x019C

    POSSIBLE_PLANCK_F_OFFSET = 0x01A0

    def __init__(self, data: bytes):
        self.data = data

    def _read_float32(self, offset: int) -> float:
        return struct.unpack(
            "<f",
            self.data[offset : offset + 4],
        )[0]

    def parse(self) -> RadiometricMetadata:
        return RadiometricMetadata(
            emissivity=self._read_float32(
                self.EMISSIVITY_OFFSET
            ),

            object_distance_m=self._read_float32(
                self.OBJECT_DISTANCE_OFFSET
            ),

            reflected_temperature_k=self._read_float32(
                self.REFLECTED_TEMP_OFFSET
            ),

            atmospheric_temperature_k=self._read_float32(
                self.ATMOSPHERIC_TEMP_OFFSET
            ),

            unknown_0174=self._read_float32(
                self.UNKNOWN_0174_OFFSET
            ),

            unknown_017C=self._read_float32(
                self.UNKNOWN_017C_OFFSET
            ),

            unknown_0180=self._read_float32(
                self.UNKNOWN_0180_OFFSET
            ),

            possible_planck_r1=self._read_float32(
                self.POSSIBLE_PLANCK_R1_OFFSET
            ),

            possible_planck_b=self._read_float32(
                self.POSSIBLE_PLANCK_B_OFFSET
            ),

            possible_planck_f=self._read_float32(
                self.POSSIBLE_PLANCK_F_OFFSET
            ),
        )