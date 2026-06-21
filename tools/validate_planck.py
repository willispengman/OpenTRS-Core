"""
OpenTRS-Core

Validate Planck temperature conversion against FLIR Tools CSV export.

Copyright (c) 2026 Willis Peng
License: Apache-2.0
"""

from pathlib import Path
import argparse
import math

import numpy as np

from opentrs.decoder.csq_decoder import CSQDecoder
from opentrs.decoder.jpeg_ls_decoder import JPEGLSDecoder


CSQ_FILE = Path("tests/data/sample.csq")
CSV_FILE = Path("tests/data/CSVwith Hesder.csv")


R1 = 16061.459961
B = 1418.900024
F = 1.0


def load_frame_number(path: Path) -> int:
    with path.open("r", encoding="utf-8-sig") as f:
        for line in f:
            if line.startswith("FrameNumber"):
                return int(line.split("=")[1].strip())

    raise RuntimeError("FrameNumber not found in CSV header.")


def load_temperature_csv(path: Path) -> np.ndarray:
    with path.open("r", encoding="utf-8-sig") as f:
        lines = f.readlines()

    start = None

    for i, line in enumerate(lines):
        if line.strip() == "":
            start = i + 1
            break

    if start is None:
        raise RuntimeError("Could not find CSV matrix.")

    return np.loadtxt(lines[start:], delimiter=",")


def raw_to_celsius(raw: np.ndarray, r2: float, o: float) -> np.ndarray:
    raw_float = raw.astype(np.float64)

    kelvin = B / np.log(
        R1 / (
            r2 * (raw_float + o)
        ) + F
    )

    return kelvin - 273.15


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--r2", type=float, required=True)
    parser.add_argument("--o", type=float, required=True)

    args = parser.parse_args()

    flir_frame_number = load_frame_number(CSV_FILE)
    opentrs_frame_index = flir_frame_number - 1

    decoder = CSQDecoder(CSQ_FILE)
    frames = list(decoder.iter_frames())

    frame = frames[opentrs_frame_index]

    raw = JPEGLSDecoder().decode(frame.jpeg_ls).data
    flir_temp = load_temperature_csv(CSV_FILE)

    opentrs_temp = raw_to_celsius(
        raw,
        r2=args.r2,
        o=args.o,
    )

    diff = opentrs_temp - flir_temp

    rmse = math.sqrt(float(np.mean(diff ** 2)))

    worst_index = np.unravel_index(
        np.argmax(np.abs(diff)),
        diff.shape,
    )

    y, x = worst_index

    print("Planck Validation")
    print("=================")
    print()
    print(f"R1 : {R1}")
    print(f"R2 : {args.r2}")
    print(f"B  : {B}")
    print(f"F  : {F}")
    print(f"O  : {args.o}")
    print()
    print(f"Pixels       : {diff.size}")
    print(f"Mean Error   : {np.mean(diff): .6f} °C")
    print(f"Median Error : {np.median(diff): .6f} °C")
    print(f"RMSE         : {rmse: .6f} °C")
    print(f"Max Abs Err  : {np.max(np.abs(diff)): .6f} °C")
    print()
    print("Worst Pixel")
    print("-----------")
    print(f"Location     : ({y}, {x})")
    print(f"Raw          : {raw[y, x]}")
    print(f"OpenTRS      : {opentrs_temp[y, x]:.6f} °C")
    print(f"FLIR         : {flir_temp[y, x]:.6f} °C")
    print(f"Difference   : {diff[y, x]:.6f} °C")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())