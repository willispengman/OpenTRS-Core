import struct

import pytest

from opentrs.metadata.model import RadiometricMetadata
from opentrs.metadata.parser import MetadataParser


def test_metadata_model_creation():
    metadata = RadiometricMetadata(
        emissivity=0.98,
        object_distance_m=2.0,
    )

    assert metadata.emissivity == 0.98
    assert metadata.object_distance_m == 2.0


def test_metadata_parser_returns_metadata():
    data = bytearray(512)

    data[0x0160:0x0164] = struct.pack("<f", 0.98)
    data[0x0164:0x0168] = struct.pack("<f", 2.0)

    parser = MetadataParser(bytes(data))

    metadata = parser.parse()

    assert isinstance(metadata, RadiometricMetadata)
    assert metadata.emissivity == pytest.approx(0.98)
    assert metadata.object_distance_m == pytest.approx(2.0)