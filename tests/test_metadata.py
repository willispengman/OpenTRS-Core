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
        possible_planck_r2=0.01150952,
        possible_planck_b=1418.9,
        possible_planck_f=1.0,
        possible_planck_o=-5027,
    )

    assert metadata.emissivity == pytest.approx(0.98)
    assert metadata.object_distance_m == pytest.approx(2.0)
    assert metadata.possible_planck_r2 == pytest.approx(0.01150952)
    assert metadata.possible_planck_o == pytest.approx(-5027)


def test_metadata_parser_returns_metadata():
    data = bytearray(4096)

    floats = {
        0x0140 + 0x0020: 0.98,
        0x0140 + 0x0024: 2.0,
        0x0140 + 0x0028: 298.15,
        0x0140 + 0x002C: 293.15,
        0x0140 + 0x0034: 1.0,
        0x0140 + 0x003C: 0.5,
        0x0140 + 0x0040: 6.0,
        0x0140 + 0x0058: 16061.46,
        0x0140 + 0x005C: 1418.9,
        0x0140 + 0x0060: 1.0,
        0x0140 + 0x030C: 0.01150952,
    }

    for offset, value in floats.items():
        data[offset:offset + 4] = struct.pack("<f", value)

    data[0x0140 + 0x0308:0x0140 + 0x030C] = struct.pack("<i", -5027)

    result = MetadataParser(bytes(data)).parse()

    assert result.emissivity == pytest.approx(0.98)
    assert result.object_distance_m == pytest.approx(2.0)
    assert result.reflected_temperature_k == pytest.approx(298.15)
    assert result.atmospheric_temperature_k == pytest.approx(293.15)

    assert result.unknown_0174 == pytest.approx(1.0)
    assert result.unknown_017C == pytest.approx(0.5)
    assert result.unknown_0180 == pytest.approx(6.0)

    assert result.possible_planck_r1 == pytest.approx(16061.46)
    assert result.possible_planck_r2 == pytest.approx(0.01150952)
    assert result.possible_planck_b == pytest.approx(1418.9)
    assert result.possible_planck_f == pytest.approx(1.0)
    assert result.possible_planck_o == pytest.approx(-5027)