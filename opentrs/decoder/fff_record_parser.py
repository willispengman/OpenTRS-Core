class FFFRecordParser:

    def __init__(self, frame_bytes: bytes):
        self.frame = frame_bytes

    def iter_records(self):
        ...