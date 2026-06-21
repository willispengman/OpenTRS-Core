"""
OpenTRS-Core

Metadata Parser

Copyright (c) 2026 Willis Peng
License: Apache-2.0
"""

from opentrs.metadata.model import RadiometricMetadata


class MetadataParser:
    """
    Parser for radiometric metadata.

    This is a skeleton for future FLIR FFF metadata parsing.
    """

    def __init__(self, data: bytes):
        self.data = data

    def parse(self) -> RadiometricMetadata:
        """
        Parse radiometric metadata from binary data.
        """
        return RadiometricMetadata()