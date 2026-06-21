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

    Offsets are based on reverse engineering of FLIR FFF record type 32.
    """

    RECORD_32_OFFSET = 0x0140

    EMISSIVITY_OFFSET = RECORD_32_OFFSET + 0x0020
    OBJECT_DISTANCE_OFFSET = RECORD_32_OFFSET + 0x0024
    REFLECTED_TEMP_OFFSET = RECORD_32_OFFSET + 0x0028
    ATMOSPHERIC_TEMP_OFFSET = RECORD_32_OFFSET + 0x002C

    UNKNOWN_0174_OFFSET = RECORD_32_OFFSET + 0x0034
    UNKNOWN_017C_OFFSET = RECORD_32_OFFSET + 0x003C
    UNKNOWN_0180_OFFSET = RECORD_32_OFFSET + 0x0040

    POSSIBLE_PLANCK_R1_OFFSET = RECORD_32_OFFSET + 0x0058
    POSSIBLE_PLANCK_B_OFFSET = RECORD_32_OFFSET + 0x005C
    POSSIBLE_PLANCK_F_OFFSET = RECORD_32_OFFSET + 0x0060

    POSSIBLE_PLANCK_O_OFFSET = RECORD_32_OFFSET + 0x0308
    POSSIBLE_PLANCK_R2_OFFSET = RECORD_32_OFFSET + 0x030C

    def __init__(self, data: bytes):
        self.data = data

    def _read_float32(self, offset: int) -> float:
        return struct.unpack("<f", self.data[offset:offset + 4])[0]

    def _read_int32(self, offset: int) -> int:
        return struct.unpack("<i", self.data[offset:offset + 4])[0]

    def parse(self) -> RadiometricMetadata:
        return RadiometricMetadata(
            emissivity=self._read_float32(self.EMISSIVITY_OFFSET),
            object_distance_m=self._read_float32(self.OBJECT_DISTANCE_OFFSET),
            reflected_temperature_k=self._read_float32(self.REFLECTED_TEMP_OFFSET),
            atmospheric_temperature_k=self._read_float32(
                self.ATMOSPHERIC_TEMP_OFFSET
            ),
            unknown_0174=self._read_float32(self.UNKNOWN_0174_OFFSET),
            unknown_017C=self._read_float32(self.UNKNOWN_017C_OFFSET),
            unknown_0180=self._read_float32(self.UNKNOWN_0180_OFFSET),
            possible_planck_r1=self._read_float32(self.POSSIBLE_PLANCK_R1_OFFSET),
            possible_planck_r2=self._read_float32(self.POSSIBLE_PLANCK_R2_OFFSET),
            possible_planck_b=self._read_float32(self.POSSIBLE_PLANCK_B_OFFSET),
            possible_planck_f=self._read_float32(self.POSSIBLE_PLANCK_F_OFFSET),
            possible_planck_o=float(self._read_int32(self.POSSIBLE_PLANCK_O_OFFSET)),
        )