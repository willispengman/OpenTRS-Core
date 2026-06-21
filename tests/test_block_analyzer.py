from opentrs.metadata.block_analyzer import BlockAnalyzer


def test_block_analysis():
    jpeg = b"\xff\xd8\xff\xf7hello\xff\xd9"

    block = (
        b"HEADER"
        + jpeg
        + b"FOOTER"
    )

    info = BlockAnalyzer(block).analyze()

    assert info.block_size == len(block)
    assert info.jpeg_offset == len(b"HEADER")
    assert info.jpeg_size == len(jpeg)