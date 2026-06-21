"""
OpenTRS

End-to-End pipeline test.
"""

from pathlib import Path
import math

import numpy as np

from opentrs.decoder.csq_decoder import CSQDecoder
from opentrs.decoder.jpeg_ls_decoder import JPEGLSDecoder
from opentrs.metadata.parser import MetadataParser
from opentrs.radiometry.planck import raw_array_to_celsius


CSQ_FILE = Path("tests/data/sample.csq")
CSV_FILE = Path("tests/data/CSVwith Hesder.csv")


def load_frame_number(path: Path) -> int:
    with path.open("r", encoding="utf-8-sig") as f:
        for line in f:
            if line.startswith("FrameNumber"):
                return int(line.split("=")[1])

    raise RuntimeError("FrameNumber not found")


def load_csv(path: Path) -> np.ndarray:
    with path.open("r", encoding="utf-8-sig") as f:
        lines = f.readlines()

    start = None

    for i, line in enumerate(lines):
        if line.strip() == "":
            start = i + 1
            break

    return np.loadtxt(lines[start:], delimiter=",")


def rmse(a, b):
    return math.sqrt(np.mean((a - b) ** 2))


def test_pipeline():
    frame_number = load_frame_number(CSV_FILE)

    decoder = CSQDecoder(CSQ_FILE)

    frames = list(decoder.iter_frames())

    frame = frames[frame_number - 1]

    raw = JPEGLSDecoder().decode(frame.jpeg_ls).data

    metadata = MetadataParser(frame.header).parse()

    temperature = raw_array_to_celsius(
        raw,
        metadata,
    )

    reference = load_csv(CSV_FILE)

    error = rmse(
        temperature,
        reference,
    )

    print(f"RMSE = {error:.6f}")

    assert error < 0.1