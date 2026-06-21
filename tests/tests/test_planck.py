import pytest

from opentrs.metadata.model import RadiometricMetadata
from opentrs.radiometry.planck import raw_to_temperature


def test_planck_not_implemented():
    metadata = RadiometricMetadata()

    with pytest.raises(NotImplementedError):
        raw_to_temperature(
            10000,
            metadata,
        )