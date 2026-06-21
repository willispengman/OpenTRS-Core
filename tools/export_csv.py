"""
OpenTRS-Core

Export CSQ temperature frames to CSV.
"""

from pathlib import Path
import argparse

import numpy as np

from opentrs.decoder.csq_decoder import CSQDecoder
from opentrs.decoder.jpeg_ls_decoder import JPEGLSDecoder
from opentrs.metadata.parser import MetadataParser
from opentrs.radiometry.planck import raw_array_to_celsius


def main() -> int:
    parser = argparse.ArgumentParser()

    parser.add_argument("input", help="Input .csq file")
    parser.add_argument(
        "-o",
        "--output",
        default="output_csv",
        help="Output folder",
    )

    args = parser.parse_args()

    input_path = Path(args.input)
    output_dir = Path(args.output)

    output_dir.mkdir(parents=True, exist_ok=True)

    decoder = CSQDecoder(input_path)
    frames = list(decoder.iter_frames())

    print(f"Input  : {input_path}")
    print(f"Frames : {len(frames)}")
    print(f"Output : {output_dir}")
    print()

    for frame in frames:
        raw = JPEGLSDecoder().decode(frame.jpeg_ls).data
        metadata = MetadataParser(frame.header).parse()

        temperature = raw_array_to_celsius(
            raw,
            metadata,
        )

        output_file = output_dir / f"frame_{frame.index:04d}.csv"

        np.savetxt(
            output_file,
            temperature,
            delimiter=",",
            fmt="%.5f",
        )

        print(f"Saved {output_file}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())