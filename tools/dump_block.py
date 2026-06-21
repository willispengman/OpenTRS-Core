"""
OpenTRS Tool

Dump basic information about the first FFF/RTP block in a CSQ file.
"""

from pathlib import Path
import sys

from opentrs.decoder.fff_parser import FFFParser
from opentrs.metadata.block_analyzer import BlockAnalyzer


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python tools/dump_block.py path/to/file.csq")
        return 1

    csq_path = Path(sys.argv[1])

    if not csq_path.exists():
        print(f"File not found: {csq_path}")
        return 1

    data = csq_path.read_bytes()

    parser = FFFParser(data)
    blocks = list(parser.iter_blocks())

    if not blocks:
        print("No FFF/RTP blocks found.")
        return 1

    block = blocks[0]
    info = BlockAnalyzer(block).analyze()

    print("OpenTRS FFF Block Dump")
    print("======================")
    print(f"Source      : {csq_path}")
    print(f"Block Count : {len(blocks)}")
    print("")
    print("First Block")
    print("-----------")
    print(f"Block Size  : {info.block_size}")
    print(f"JPEG Offset : {info.jpeg_offset}")
    print(f"JPEG Size   : {info.jpeg_size}")
    print(f"Header Size : {info.jpeg_offset}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())