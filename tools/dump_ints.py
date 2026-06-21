"""
OpenTRS-Core

Dump int32 values from the first FFF block.

Copyright (c) 2026 Willis Peng
License: Apache-2.0
"""

from pathlib import Path
import struct
import sys

from opentrs.decoder.fff_parser import FFFParser


HEADER_SIZE = 3796


def main() -> int:

    if len(sys.argv) != 2:
        print(
            "Usage:\n"
            "python -m tools.dump_ints file.csq"
        )
        return 1

    path = Path(sys.argv[1])

    parser = FFFParser(path.read_bytes())

    block = next(parser.iter_blocks())

    print("Possible int32 values")
    print("=====================")

    for offset in range(0, HEADER_SIZE - 4, 4):

        value = struct.unpack(
            "<i",
            block[offset:offset + 4],
        )[0]

        # Skip zero values
        if value == 0:
            continue

        # Skip obvious pointers / sizes
        if abs(value) > 100_000_000:
            continue

        print(
            f"0x{offset:04X} : {value:12d}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())