"""
OpenTRS-Core

CSQ Decoder

Copyright (c) 2026 Willis Peng
License: Apache-2.0
"""

from pathlib import Path
from typing import Iterator

from opentrs.decoder.fff_parser import FFFParser

JPEG_LS_SIGNATURE = b"\xff\xd8\xff\xf7"
JPEG_END_SIGNATURE = b"\xff\xd9"


class CSQFrame:
    """
    One extracted frame from a CSQ file.
    """

    def __init__(self, index: int, block: bytes, jpeg_ls: bytes):
        self.index = index
        self.block = block
        self.header = block
        self.jpeg_ls = jpeg_ls


class CSQDecoder:
    """
    Entry point for reading FLIR CSQ files.
    """

    def __init__(self, filename: str | Path):
        self.path = Path(filename)

    @property
    def filename(self) -> str:
        return str(self.path)

    def exists(self) -> bool:
        return self.path.exists()

    def open(self) -> None:
        if not self.exists():
            raise FileNotFoundError(f"CSQ file not found: {self.path}")

        print(f"Opening CSQ file: {self.path}")

    def iter_frames(self) -> Iterator[CSQFrame]:
        if not self.exists():
            raise FileNotFoundError(f"CSQ file not found: {self.path}")

        data = self.path.read_bytes()
        parser = FFFParser(data)

        for block_index, block in enumerate(parser.iter_blocks()):
            start = block.find(JPEG_LS_SIGNATURE)

            if start < 0:
                continue

            end = block.find(JPEG_END_SIGNATURE, start)

            if end < 0:
                continue

            yield CSQFrame(
                index=block_index,
                block=block,
                jpeg_ls=block[start:end + len(JPEG_END_SIGNATURE)],
            )