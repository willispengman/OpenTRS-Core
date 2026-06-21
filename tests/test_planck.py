import pytest

from opentrs.metadata.model import RadiometricMetadata
from opentrs.radiometry.planck import raw_to_kelvin


def test_missing_planck_constants():
    metadata = RadiometricMetadata()

    with pytest.raises(ValueError):
        raw_to_kelvin(
            10000,
            metadata,
        )