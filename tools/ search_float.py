"""
Search a float value inside metadata.
"""

import struct
from pathlib import Path

from opentrs.trs.reader import TRSReader


TARGET = 16061.459961

reader = TRSReader(Path("tests/data/sample.csq"))

value = struct.pack("<f", TARGET)

for frame in reader.frames:

    for block in frame.blocks:

        idx = block.data.find(value)

        if idx != -1:

            print()

            print("Found!")

            print("Block type :", block.block_type)

            print("Offset     :", hex(idx))