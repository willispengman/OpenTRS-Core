"""
OpenTRS Tool

Dump consecutive float32 values from the first FFF block.
"""

from pathlib import Path
import struct
import sys

from opentrs.decoder.fff_parser import FFFParser


def main() -> int:

    if len(sys.argv) != 4:
        print(
            "Usage:\n"
            "python -m tools.dump_floats file.csq offset count"
        )
        return 1

    path = Path(sys.argv[1])

    offset = int(sys.argv[2], 0)

    count = int(sys.argv[3])

    data = path.read_bytes()

    parser = FFFParser(data)

    block = next(parser.iter_blocks())

    print(f"Offset  : 0x{offset:04X}")
    print(f"Floats  : {count}")
    print()

    for i in range(count):

        current = offset + i * 4

        value = struct.unpack(
            "<f",
            block[current:current + 4],
        )[0]

        print(
            f"0x{current:04X} : {value:12.6f}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())