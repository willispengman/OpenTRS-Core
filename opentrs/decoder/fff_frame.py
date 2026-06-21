from dataclasses import dataclass

@dataclass(slots=True)
class FFFRecord:
    record_type: int
    offset: int
    size: int
    data: bytes


@dataclass(slots=True)
class FFFFrame:
    index: int

    raw: bytes

    header: bytes

    metadata: bytes

    records: list[FFFRecord]

    jpeg_ls: bytes