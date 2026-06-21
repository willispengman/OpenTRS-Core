import pytest

from opentrs.decoder.jpeg_ls_decoder import JPEGLSDecoder


def test_find_ffmpeg():
    decoder = JPEGLSDecoder()

    assert decoder.ffmpeg_path


def test_decode_invalid_jpeg_ls_raises_error():
    decoder = JPEGLSDecoder()

    with pytest.raises(RuntimeError):
        decoder.decode(b"not jpeg ls")