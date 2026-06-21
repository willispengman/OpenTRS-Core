from opentrs.decoder.fff_parser import FFFParser


def test_empty_file():

    parser = FFFParser(b"")

    assert parser.find_blocks() == []