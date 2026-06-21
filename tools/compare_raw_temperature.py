"""
OpenTRS-Core

Compare OpenTRS Raw Values with FLIR Tools Temperature Export

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
        raise RuntimeError(
            "Could not locate the beginning of the temperature matrix."
        )

    return np.loadtxt(lines[start:], delimiter=",")


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

    print("Comparison")
    print("==========")
    print()

    print(f"Frame Count        : {len(frames)}")
    print(f"FLIR FrameNumber   : {flir_frame_number}")
    print(f"OpenTRS frame index: {opentrs_frame_index}")
    print()

    frame = frames[opentrs_frame_index]

    raw = JPEGLSDecoder().decode(frame.jpeg_ls).data
    temperature = load_temperature_csv(CSV_FILE)

    print(f"Raw Shape : {raw.shape}")
    print(f"CSV Shape : {temperature.shape}")
    print()

    if raw.shape != temperature.shape:
        print("WARNING: Shape mismatch!")
        return

    samples = [
        (0, 0),
        (0, raw.shape[1] - 1),
        (raw.shape[0] // 2, raw.shape[1] // 2),
        (raw.shape[0] - 1, 0),
        (raw.shape[0] - 1, raw.shape[1] - 1),
    ]

    print("Sample Pixels")
    print("-------------")

    for y, x in samples:
        print(
            f"({y:3d}, {x:3d})"
            f"   Raw = {raw[y, x]:5d}"
            f"   Temp = {temperature[y, x]:7.3f} °C"
        )


if __name__ == "__main__":
    main()