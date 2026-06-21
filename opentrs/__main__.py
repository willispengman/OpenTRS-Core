"""
OpenTRS-Core CLI
"""

from pathlib import Path
import argparse

from opentrs.tools.export import export_sequence


def main():
    parser = argparse.ArgumentParser(
        prog="opentrs",
        description="CSQ thermal sequence exporter",
    )

    parser.add_argument(
        "input",
        type=str,
        help="Input CSQ file",
    )

    parser.add_argument(
        "--out",
        type=str,
        default="output",
        help="Output directory",
    )

    parser.add_argument(
        "--palette",
        type=str,
        default="gray",
        choices=["gray", "iron"],
        help="Color palette",
    )

    parser.add_argument(
        "--min",
        type=float,
        default=20.0,
        help="Temperature min (C)",
    )

    parser.add_argument(
        "--max",
        type=float,
        default=40.0,
        help="Temperature max (C)",
    )

    args = parser.parse_args()

    export_sequence(
        input_path=Path(args.input),
        output_dir=Path(args.out),
        palette=args.palette,
        tmin=args.min,
        tmax=args.max,
    )


if __name__ == "__main__":
    main()