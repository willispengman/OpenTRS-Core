from pathlib import Path

from opentrs.decoder.fff_parser import FFFParser

CSQ = "tests/data/sample.csq"

FRAME = 83
OFFSET = 320
SIZE = 2476


def main():
    data = Path(CSQ).read_bytes()

    block = list(FFFParser(data).iter_blocks())[FRAME]

    record = block[OFFSET:OFFSET + SIZE]

    print(f"Record size: {len(record)} bytes\n")

    for i in range(0, len(record), 16):
        chunk = record[i:i+16]

        print(
            f"{i:04X} : "
            + " ".join(f"{b:02X}" for b in chunk)
        )


if __name__ == "__main__":
    main()