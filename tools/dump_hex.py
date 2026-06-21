"""
OpenTRS Tool

Hex dump the first bytes of a FLIR FFF/RTP block.
"""

from pathlib import Path
import sys

from opentrs.decoder.fff_parser import FFFParser


BYTES_PER_LINE = 16


def hex_dump(data: bytes, limit: int = 512) -> None:
    """
    Print a hexadecimal dump.
    """
    data = data[:limit]

    for offset in range(0, len(data), BYTES_PER_LINE):
        chunk = data[offset : offset + BYTES_PER_LINE]

        hex_part = " ".join(f"{b:02X}" for b in chunk)
        ascii_part = "".join(
            chr(b) if 32 <= b <= 126 else "."
            for b in chunk
        )

        print(
            f"{offset:08X}  "
            f"{hex_part:<47}  "
            f"{ascii_part}"
        )


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage:")
        print("python -m tools.dump_hex path/to/file.csq")
        return 1

    path = Path(sys.argv[1])

    if not path.exists():
        print(f"File not found: {path}")
        return 1

    data = path.read_bytes()

    parser = FFFParser(data)
    blocks = list(parser.iter_blocks())

    if not blocks:
        print("No FFF/RTP blocks found.")
        return 1

    print("First FFF Block")
    print("================")
    print(f"Size : {len(blocks[0])} bytes")
    print()

    hex_dump(blocks[0])

    return 0


if __name__ == "__main__":
    raise SystemExit(main())