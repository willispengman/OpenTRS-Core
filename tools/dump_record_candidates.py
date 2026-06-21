"""
OpenTRS-Core

Dump possible FFF record directory entries.
"""

from pathlib import Path
import struct

from opentrs.decoder.fff_parser import FFFParser


CSQ_FILE = Path("tests/data/sample.csq")
FRAME_INDEX = 83

ENTRY_START = 0x40
ENTRY_END = 0x140
ENTRY_SIZE = 0x20


def u16(data: bytes, offset: int) -> int:
    return struct.unpack("<H", data[offset : offset + 2])[0]


def u32(data: bytes, offset: int) -> int:
    return struct.unpack("<I", data[offset : offset + 4])[0]


def main() -> int:
    data = CSQ_FILE.read_bytes()
    blocks = list(FFFParser(data).iter_blocks())

    block = blocks[FRAME_INDEX]

    print("Possible FFF Record Directory")
    print("=============================")
    print()
    print(f"Frame index : {FRAME_INDEX}")
    print(f"Block size  : {len(block)}")
    print()

    print(
        "entry_offset  "
        "type  subtype  value_a  value_b  offset  size"
    )
    print("-" * 70)

    for entry_offset in range(ENTRY_START, ENTRY_END, ENTRY_SIZE):
        record_type = u16(block, entry_offset)
        subtype = u16(block, entry_offset + 2)
        value_a = u32(block, entry_offset + 4)
        value_b = u32(block, entry_offset + 8)
        offset = u32(block, entry_offset + 12)
        size = u32(block, entry_offset + 16)

        print(
            f"0x{entry_offset:04X}        "
            f"{record_type:4d}  "
            f"{subtype:7d}  "
            f"{value_a:7d}  "
            f"{value_b:7d}  "
            f"{offset:6d}  "
            f"{size:6d}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())