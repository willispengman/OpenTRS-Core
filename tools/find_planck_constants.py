"""
OpenTRS-Core

Find Possible Planck Constants

Copyright (c) 2026 Willis Peng
License: Apache-2.0
"""

from pathlib import Path
import struct
import sys

from opentrs.decoder.fff_parser import FFFParser


HEADER_SIZE = 3796


def main():

    if len(sys.argv) != 2:
        print(
            "Usage:\n"
            "python -m tools.find_planck_constants file.csq"
        )
        return

    path = Path(sys.argv[1])

    parser = FFFParser(path.read_bytes())

    block = next(parser.iter_blocks())

    print("Possible float32 values")
    print("=======================")

    for offset in range(0, HEADER_SIZE - 4, 4):

        value = struct.unpack(
            "<f",
            block[offset:offset + 4],
        )[0]

        if abs(value) < 1e-8:
            continue

        if abs(value) > 1e30:
            continue

        print(
            f"0x{offset:04X} : {value:15.6f}"
        )


if __name__ == "__main__":
    main()