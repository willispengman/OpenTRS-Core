import numpy as np

from opentrs.trs.raw_frame import RawFrame


def test_raw_frame_creation():
    data = np.zeros((288, 384), dtype=np.uint16)

    frame = RawFrame(
        width=384,
        height=288,
        data=data,
    )

    assert frame.width == 384
    assert frame.height == 288
    assert frame.shape == (288, 384)
    assert frame.dtype == np.uint16