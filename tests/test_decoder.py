from pathlib import Path

import pytest

from opentrs.decoder.csq_decoder import CSQDecoder


def test_decoder_creation():
    decoder = CSQDecoder("example.csq")

    assert decoder.filename == "example.csq"


def test_missing_file_raises_error():
    decoder = CSQDecoder("missing.csq")

    with pytest.raises(FileNotFoundError):
        list(decoder.iter_frames())


def test_iter_frames_extracts_jpeg_ls(tmp_path: Path):
    csq = tmp_path / "sample.csq"

    fake_jpeg_ls = b"\xff\xd8\xff\xf7hello\xff\xd9"

    csq.write_bytes(
        b"noise"
        + b"FFF\x00RTP\x00"
        + b"block-header"
        + fake_jpeg_ls
        + b"tail"
    )

    decoder = CSQDecoder(str(csq))
    frames = list(decoder.iter_frames())

    assert len(frames) == 1
    assert frames[0].index == 0
    assert frames[0].jpeg_ls == fake_jpeg_ls