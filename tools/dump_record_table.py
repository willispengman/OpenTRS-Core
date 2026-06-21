from pathlib import Path

from opentrs.decoder.csq_decoder import CSQDecoder
from opentrs.decoder.fff_record_parser import FFFRecordParser


CSQ = Path("tests/data/sample.csq")


def main():

    decoder = CSQDecoder(CSQ)

    frame = decoder.frames[83]

    parser = FFFRecordParser(frame.data)

    print("Record Table")
    print("============")

    for i, record in enumerate(parser.iter_records()):

        print(
            f"{i:02d}  "
            f"type={record.record_type:4d}  "
            f"sub={record.record_subtype:4d}  "
            f"offset={record.offset:6d}  "
            f"size={record.size:6d}"
        )


if __name__ == "__main__":
    main()