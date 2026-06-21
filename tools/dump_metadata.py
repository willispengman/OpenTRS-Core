"""
OpenTRS-Core

Dump parsed metadata from sample CSQ.

Copyright (c) 2026 Willis Peng
License: Apache-2.0
"""

from pathlib import Path

from opentrs.decoder.fff_parser import FFFParser
from opentrs.metadata.parser import MetadataParser


CSQ_FILE = Path("tests/data/sample.csq")


def main() -> int:
    data = CSQ_FILE.read_bytes()

    parser = FFFParser(data)
    blocks = list(parser.iter_blocks())

    block = blocks[83]

    metadata = MetadataParser(block).parse()

    print("Metadata")
    print("========")
    print()

    for field in metadata.__dataclass_fields__:
        value = getattr(metadata, field)
        print(f"{field:30s}: {value}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())