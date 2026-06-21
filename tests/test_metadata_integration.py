import pytest

from opentrs.decoder.fff_parser import FFFParser
from opentrs.metadata.parser import MetadataParser


def test_sample_csq_metadata_candidates():
    data = open("tests/data/sample.csq", "rb").read()

    block = next(FFFParser(data).iter_blocks())

    metadata = MetadataParser(block).parse()

    assert metadata.emissivity == pytest.approx(0.98)
    assert metadata.object_distance_m == pytest.approx(2.0)

    assert metadata.reflected_temperature_k == pytest.approx(298.15)
    assert metadata.atmospheric_temperature_k == pytest.approx(293.15)

    assert metadata.possible_planck_r1 == pytest.approx(16061.46, rel=1e-4)
    assert metadata.possible_planck_b == pytest.approx(1418.9, rel=1e-4)
    assert metadata.possible_planck_f == pytest.approx(1.0)