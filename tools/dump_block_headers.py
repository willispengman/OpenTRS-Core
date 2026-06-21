"""
Print every FFF block header.
"""

from pathlib import Path

from opentrs.trs.reader import TRSReader


CSQ = Path("tests/data/sample.csq")


def main():

    reader = TRSReader(CSQ)

    for frame_index, frame in enumerate(reader.frames):

        print(f"\nFrame {frame_index}")
        print("----------------------")

        for block in frame.blocks:

            print(vars(block))


if __name__ == "__main__":
    main()