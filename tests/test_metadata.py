import struct

import pytest

from opentrs.metadata.model import RadiometricMetadata
from opentrs.metadata.parser import MetadataParser


def test_metadata_model_creation():
    metadata = RadiometricMetadata(
        emissivity=0.98,
        object_distance_m=2.0,
        reflected_temperature_k=298.15,
        atmospheric_temperature_k=293.15,
        possible_planck_r1=16061.46,
        possible_planck_b=1418.9,
        possible_planck_f=1.0,
    )

    assert metadata.emissivity == pytest.approx(0.98)
    assert metadata.object_distance_m == pytest.approx(2.0)


def test_metadata_parser_returns_metadata():
    data = bytearray(1024)

    values = {
        0x0160: 0.98,
        0x0164: 2.0,
        0x0168: 298.15,
        0x016C: 293.15,
        0x0174: 1.0,
        0x017C: 0.5,
        0x0180: 6.0,
        0x0198: 16061.46,
        0x019C: 1418.9,
        0x01A0: 1.0,
    }

    for offset, value in values.items():
        data[offset : offset + 4] = struct.pack("<f", value)

    metadata = MetadataParser(bytes(data))

    result = metadata.parse()

    assert result.emissivity == pytest.approx(0.98)
    assert result.object_distance_m == pytest.approx(2.0)

    assert result.reflected_temperature_k == pytest.approx(298.15)
    assert result.atmospheric_temperature_k == pytest.approx(293.15)

    assert result.unknown_0174 == pytest.approx(1.0)
    assert result.unknown_017C == pytest.approx(0.5)
    assert result.unknown_0180 == pytest.approx(6.0)

    assert result.possible_planck_r1 == pytest.approx(16061.46)
    assert result.possible_planck_b == pytest.approx(1418.9)
    assert result.possible_planck_f == pytest.approx(1.0)