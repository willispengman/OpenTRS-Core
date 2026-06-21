"""
Dump every float inside metadata.
"""

import struct

from pathlib import Path

from opentrs.trs.reader import TRSReader


reader = TRSReader(Path("tests/data/sample.csq"))

frame = reader.frames[0]

for block in frame.blocks:

    print()
    print("BLOCK", block.block_type)

    for offset in range(0, len(block.data) - 4, 4):

        value = struct.unpack(
            "<f",
            block.data[offset:offset+4],
        )[0]

        if abs(value) < 100000:

            print(
                f"{offset:04X}",
                value,
            )