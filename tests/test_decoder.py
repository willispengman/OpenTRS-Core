from opentrs.decoder.csq_decoder import CSQDecoder


def test_decoder_creation():
    decoder = CSQDecoder("example.csq")

    assert decoder.filename == "example.csq"