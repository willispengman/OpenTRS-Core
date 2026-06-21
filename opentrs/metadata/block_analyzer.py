"""
OpenTRS-Core

FFF Block Analyzer

Copyright (c) 2026 Willis Peng
License: Apache-2.0
"""

from dataclasses import dataclass

JPEG_LS_SIGNATURE = b"\xff\xd8\xff\xf7"
JPEG_END_SIGNATURE = b"\xff\xd9"


@dataclass(slots=True)
class BlockInfo:
    block_size: int
    jpeg_offset: int
    jpeg_size: int


class BlockAnalyzer:
    """
    Analyze one FFF/RTP block.
    """

    def __init__(self, block: bytes):
        self.block = block

    def analyze(self) -> BlockInfo:
        start = self.block.find(JPEG_LS_SIGNATURE)

        if start < 0:
            raise RuntimeError("JPEG-LS start marker not found.")

        end = self.block.find(
            JPEG_END_SIGNATURE,
            start,
        )

        if end < 0:
            raise RuntimeError("JPEG-LS end marker not found.")

        return BlockInfo(
            block_size=len(self.block),
            jpeg_offset=start,
            jpeg_size=end + len(JPEG_END_SIGNATURE) - start,
        )