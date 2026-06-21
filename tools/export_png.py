"""
Export CSQ to temperature-based PNG sequence.
"""

from pathlib import Path
import sys

from opentrs.decoder.csq_decoder import CSQDecoder
from opentrs.decoder.jpeg_ls_decoder import JPEGLSDecoder
from opentrs.export.png import save_png
from opentrs.metadata.parser import MetadataParser
from opentrs.palette.gray import render_gray
from opentrs.radiometry.planck import raw_array_to_celsius


TEMP_MIN = 20.0
TEMP_MAX = 40.0


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage:")
        print("python -m tools.export_png movie.csq")
        return 1

    csq = Path(sys.argv[1])
    outdir = Path("output")
    outdir.mkdir(exist_ok=True)

    decoder = CSQDecoder(csq)
    jpeg = JPEGLSDecoder()

    count = 0

    for frame in decoder.iter_frames():
        raw = jpeg.decode(frame.jpeg_ls).data

        metadata = MetadataParser(frame.header).parse()

        temperature = raw_array_to_celsius(
            raw,
            metadata,
        )

        image = render_gray(
            temperature,
            minimum=TEMP_MIN,
            maximum=TEMP_MAX,
        )

        filename = outdir / f"{count:06d}.png"

        save_png(
            image,
            filename,
        )

        count += 1

        if count % 10 == 0:
            print(count)

    print()
    print(f"Finished {count} frames.")
    print(f"Temperature range: {TEMP_MIN:.1f}C to {TEMP_MAX:.1f}C")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())