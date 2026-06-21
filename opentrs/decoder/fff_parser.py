"""
OpenTRS-Core

FFF Block Parser

Copyright (c) 2026 Willis Peng
License: Apache-2.0
"""

from typing import Iterator

FFF_SIGNATURE = b"FFF\x00RTP\x00"


class FFFParser:
    """
    Parser for FLIR FFF/RTP blocks.
    """

    def __init__(self, data: bytes):
        self.data = data

    def find_blocks(self) -> list[int]:
        offsets: list[int] = []

        start = 0

        while True:
            index = self.data.find(
                FFF_SIGNATURE,
                start,
            )

            if index < 0:
                break

            offsets.append(index)

            start = index + 1

        return offsets

    def iter_blocks(self) -> Iterator[bytes]:
        offsets = self.find_blocks()

        bounds = offsets + [len(self.data)]

        for i, start in enumerate(offsets):
            end = bounds[i + 1]

            yield self.data[start:end]