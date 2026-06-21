import numpy as np

from opentrs.trs.frame import TRSFrame


def test_frame_creation():

    temperature = np.zeros((2, 3), dtype=np.float32)

    frame = TRSFrame(
        width=3,
        height=2,
        temperature=temperature,
    )

    assert frame.width == 3
    assert frame.height == 2

    assert frame.temperature.shape == (2, 3)