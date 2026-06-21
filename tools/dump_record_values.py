"""
OpenTRS-Core

Dump interpreted values from a selected FFF record.
"""

from pathlib import Path
import struct
import math

from opentrs.decoder.fff_parser import FFFParser


CSQ = "tests/data/sample.csq"
FRAME = 83
OFFSET = 320
SIZE = 2476


def read_float(data: bytes, offset: int) -> float:
    return struct.unpack("<f", data[offset:offset + 4])[0]


def read_int32(data: bytes, offset: int) -> int:
    return struct.unpack("<i", data[offset:offset + 4])[0]


def is_interesting_float(value: float) -> bool:
    if math.isnan(value) or math.isinf(value):
        return False

    if value == 0:
        return False

    return (
        -10000 < value < 100000
    )


def main() -> int:
    data = Path(CSQ).read_bytes()
    block = list(FFFParser(data).iter_blocks())[FRAME]
    record = block[OFFSET:OFFSET + SIZE]

    print("Record Values")
    print("=============")
    print(f"Frame  : {FRAME}")
    print(f"Offset : {OFFSET}")
    print(f"Size   : {SIZE}")
    print()

    print("Floats")
    print("------")

    for offset in range(0, len(record) - 4, 4):
        value = read_float(record, offset)

        if is_interesting_float(value):
            print(f"0x{offset:04X} : {value:15.8f}")

    print()
    print("Int32")
    print("-----")

    for offset in range(0, len(record) - 4, 4):
        value = read_int32(record, offset)

        if value == 0:
            continue

        if -100000 < value < 100000:
            print(f"0x{offset:04X} : {value:10d}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())