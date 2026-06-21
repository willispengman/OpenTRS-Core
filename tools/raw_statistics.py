"""
OpenTRS-Core

Raw Frame Statistics

Copyright (c) 2026 Willis Peng
License: Apache-2.0
"""

from pathlib import Path

from opentrs.decoder.csq_decoder import CSQDecoder
from opentrs.decoder.jpeg_ls_decoder import JPEGLSDecoder


def main():
    decoder = CSQDecoder(
        Path("tests/data/sample.csq")
    )

    frame = next(decoder.iter_frames())

    raw = JPEGLSDecoder().decode(
        frame.jpeg_ls
    )

    data = raw.data

    print("Raw Statistics")
    print("================")
    print()

    print(f"Shape : {raw.shape}")
    print(f"dtype : {raw.dtype}")

    print()

    print(f"Min   : {data.min()}")
    print(f"Max   : {data.max()}")
    print(f"Mean  : {data.mean():.2f}")
    print(f"Std   : {data.std():.2f}")


if __name__ == "__main__":
    main()