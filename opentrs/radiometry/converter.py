"""
OpenTRS-Core

Radiometric Converter

Copyright (c) 2026 Willis Peng
License: Apache-2.0
"""

from opentrs.metadata.model import RadiometricMetadata
from opentrs.trs.raw_frame import RawFrame
from opentrs.trs.frame import TRSFrame


class RadiometricConverter:
    """
    Convert raw sensor values into temperature.
    """

    def convert(
        self,
        raw_frame: RawFrame,
        metadata: RadiometricMetadata,
    ) -> TRSFrame:
        """
        Convert one RawFrame into a temperature frame.

        This is currently a placeholder implementation.
        """

        raise NotImplementedError(
            "Radiometric conversion has not been implemented yet."
        )