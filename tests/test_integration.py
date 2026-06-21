from opentrs.decoder.csq_decoder import CSQDecoder


def test_sample_file_contains_frames():
    decoder = CSQDecoder("tests/data/sample.csq")

    frames = list(decoder.iter_frames())

    assert len(frames) > 0