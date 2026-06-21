"""
OpenTRS-Core

Check alignment between decoded raw image and FLIR Tools CSV.

Copyright (c) 2026 Willis Peng
License: Apache-2.0
"""

from pathlib import Path

import numpy as np

from opentrs.decoder.csq_decoder import CSQDecoder
from opentrs.decoder.jpeg_ls_decoder import JPEGLSDecoder


CSQ_FILE = Path("tests/data/sample.csq")
CSV_FILE = Path("tests/data/CSVwith Hesder.csv")


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


def correlation(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.corrcoef(a.ravel(), b.ravel())[0, 1])


def main():
    flir_frame_number = load_frame_number(CSV_FILE)
    opentrs_frame_index = flir_frame_number - 1

    if opentrs_frame_index < 0:
        raise RuntimeError("Invalid FLIR FrameNumber.")

    decoder = CSQDecoder(CSQ_FILE)
    frames = list(decoder.iter_frames())

    if opentrs_frame_index >= len(frames):
        raise RuntimeError(
            f"Frame index out of range: {opentrs_frame_index}"
        )

    print(f"Frame count        : {len(frames)}")
    print(f"FLIR FrameNumber   : {flir_frame_number}")
    print(f"OpenTRS frame index: {opentrs_frame_index}")
    print()

    frame = frames[opentrs_frame_index]

    raw = JPEGLSDecoder().decode(frame.jpeg_ls).data.astype(np.float64)
    temp = load_temperature_csv(CSV_FILE).astype(np.float64)

    print("Shapes")
    print("======")
    print(raw.shape)
    print(temp.shape)
    print()

    candidates = {
        "normal": temp,
        "flip_x": np.fliplr(temp),
        "flip_y": np.flipud(temp),
        "flip_xy": np.flipud(np.fliplr(temp)),
    }

    print("Correlation")
    print("===========")

    for name, img in candidates.items():
        if img.shape != raw.shape:
            print(f"{name:20s}  shape mismatch")
            continue

        print(f"{name:20s} {correlation(raw, img): .6f}")

    print()
    print("Neighbor Frames")
    print("===============")

    for neighbor in [
        opentrs_frame_index - 1,
        opentrs_frame_index,
        opentrs_frame_index + 1,
    ]:
        if neighbor < 0 or neighbor >= len(frames):
            continue

        neighbor_raw = JPEGLSDecoder().decode(
            frames[neighbor].jpeg_ls
        ).data.astype(np.float64)

        print(
            f"frame {neighbor:3d}"
            f"  normal correlation = {correlation(neighbor_raw, temp): .6f}"
        )


if __name__ == "__main__":
    main()