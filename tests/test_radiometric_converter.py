import pytest

from opentrs.metadata.model import RadiometricMetadata

from opentrs.radiometry.converter import RadiometricConverter

from opentrs.trs.raw_frame import RawFrame

import numpy as np

def test_converter_not_implemented():

    raw = RawFrame(

        width=1,

        height=1,

        data=np.zeros((1, 1), dtype=np.uint16),

    )

    metadata = RadiometricMetadata()

    converter = RadiometricConverter()

    with pytest.raises(NotImplementedError):

        converter.convert(raw, metadata)