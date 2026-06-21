"""
OpenTRS-Core

CSQ Decoder

Copyright (c) 2026 Willis Peng
License: Apache-2.0
"""

from pathlib import Path


class CSQDecoder:
    """
    Entry point for reading FLIR CSQ files.
    """

    def __init__(self, filename: str):
        self.path = Path(filename)

    @property
    def filename(self) -> str:
        """
        Return the original filename as a string.
        """
        return str(self.path)

    def exists(self) -> bool:
        """
        Return True if the CSQ file exists.
        """
        return self.path.exists()

    def open(self) -> None:
        """
        Open the CSQ file.
        """
        if not self.exists():
            raise FileNotFoundError(f"CSQ file not found: {self.path}")

        print(f"Opening CSQ file: {self.path}")