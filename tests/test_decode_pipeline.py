from opentrs.decoder.csq_decoder import CSQDecoder
from opentrs.decoder.jpeg_ls_decoder import JPEGLSDecoder
from opentrs.trs.raw_frame import RawFrame


def test_decode_first_frame():
    decoder = CSQDecoder("tests/data/sample.csq")

    frame = next(decoder.iter_frames())

    jpeg = JPEGLSDecoder()

    raw = jpeg.decode(frame.jpeg_ls)

    assert isinstance(raw, RawFrame)

    assert raw.width > 0
    assert raw.height > 0

    assert raw.data.shape == (raw.height, raw.width)

    assert raw.data.dtype.name == "uint16"