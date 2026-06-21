"""
OpenTRS-Core

Optimize Planck R2 with fixed O candidate.

Copyright (c) 2026 Willis Peng
License: Apache-2.0
"""

from pathlib import Path
import math

import numpy as np

from opentrs.decoder.csq_decoder import CSQDecoder
from opentrs.decoder.jpeg_ls_decoder import JPEGLSDecoder


CSQ_FILE = Path("tests/data/sample.csq")
CSV_FILE = Path("tests/data/CSVwith Hesder.csv")

R1 = 16061.459961
B = 1418.900024
F = 1.0

FIXED_O = -5027.0


def load_frame_number(path: Path) -> int:
    with path.open("r", encoding="utf-8-sig") as f:
        for line in f:
            if line.startswith("FrameNumber"):
                return int(line.split("=")[1].strip())

    raise RuntimeError("FrameNumber not found.")


def load_temperature_csv(path: Path) -> np.ndarray:
    with path.open("r", encoding="utf-8-sig") as f:
        lines = f.readlines()

    start = None

    for i, line in enumerate(lines):
        if line.strip() == "":
            start = i + 1
            break

    if start is None:
        raise RuntimeError("CSV matrix not found.")

    return np.loadtxt(lines[start:], delimiter=",")


def raw_to_celsius(
    raw: np.ndarray,
    r2: float,
    o: float,
) -> np.ndarray:
    raw_float = raw.astype(np.float64)

    denominator = r2 * (raw_float + o)

    with np.errstate(divide="ignore", invalid="ignore"):
        kelvin = B / np.log(
            R1 / denominator + F
        )

    return kelvin - 273.15


def rmse(a: np.ndarray, b: np.ndarray) -> float:
    diff = a - b

    valid = np.isfinite(diff)

    if not np.any(valid):
        return float("inf")

    return math.sqrt(
        float(
            np.mean(
                diff[valid] ** 2
            )
        )
    )


def main() -> int:
    frame_number = load_frame_number(CSV_FILE)

    decoder = CSQDecoder(CSQ_FILE)
    frames = list(decoder.iter_frames())

    raw = JPEGLSDecoder().decode(
        frames[frame_number - 1].jpeg_ls
    ).data

    flir = load_temperature_csv(CSV_FILE)

    best_rmse = float("inf")
    best_r2 = None

    print("Searching R2 with fixed O")
    print("=========================")
    print()
    print(f"Fixed O = {FIXED_O}")
    print()

    r2_values = np.linspace(
        0.005,
        0.03,
        500,
    )

    for r2 in r2_values:
        if np.min(raw.astype(np.float64) + FIXED_O) <= 0:
            continue

        temp = raw_to_celsius(
            raw,
            r2,
            FIXED_O,
        )

        e = rmse(
            temp,
            flir,
        )

        if e < best_rmse:
            best_rmse = e
            best_r2 = r2

            print(
                f"RMSE={e:8.5f}"
                f"   R2={r2:.8f}"
                f"   O={FIXED_O:.2f}"
            )

    print()
    print("==========")
    print("Best")
    print("==========")

    if best_r2 is None:
        print("No valid result found.")
        return 1

    print(f"R2   = {best_r2:.8f}")
    print(f"O    = {FIXED_O:.2f}")
    print(f"RMSE = {best_rmse:.6f}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())