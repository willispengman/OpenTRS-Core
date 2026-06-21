"""
OpenTRS Tool

Inspect values inside the first FFF block.
"""

from pathlib import Path
import struct
import sys

from opentrs.decoder.fff_parser import FFFParser


def inspect(data: bytes, offset: int) -> None:
    print(f"Offset : 0x{offset:04X}")
    print()

    chunk = data[offset : offset + 16]

    print("Hex")
    print("----")
    print(" ".join(f"{b:02X}" for b in chunk))
    print()

    if len(chunk) >= 2:
        print(f"uint16 : {struct.unpack('<H', chunk[:2])[0]}")

    if len(chunk) >= 4:
        print(f"uint32 : {struct.unpack('<I', chunk[:4])[0]}")
        print(f"float32: {struct.unpack('<f', chunk[:4])[0]}")

    if len(chunk) >= 8:
        print(f"double : {struct.unpack('<d', chunk[:8])[0]}")


def main() -> int:

    if len(sys.argv) != 3:
        print(
            "Usage:\n"
            "python -m tools.inspect_block file.csq offset"
        )
        return 1

    path = Path(sys.argv[1])

    offset = int(sys.argv[2], 0)

    data = path.read_bytes()

    parser = FFFParser(data)

    block = next(parser.iter_blocks())

    inspect(block, offset)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())