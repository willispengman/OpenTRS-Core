"""
OpenTRS-Core

JPEG-LS Decoder

Copyright (c) 2026 Willis Peng
License: Apache-2.0
"""

import os
import shutil
import subprocess
from pathlib import Path

import numpy as np

from opentrs.trs.raw_frame import RawFrame


class JPEGLSDecoder:
    """
    Decode JPEG-LS bytes into raw thermal frames.
    """

    def __init__(self, ffmpeg_path: str | None = None):
        self.ffmpeg_path = ffmpeg_path or self.find_ffmpeg()

    @staticmethod
    def find_ffmpeg() -> str:
        candidates = [
            os.environ.get("FFMPEG_PATH", ""),
            "/usr/local/bin/ffmpeg",
            "/opt/homebrew/bin/ffmpeg",
            "/opt/local/bin/ffmpeg",
            shutil.which("ffmpeg") or "",
        ]

        for candidate in candidates:
            if candidate and Path(candidate).exists():
                return candidate

        raise RuntimeError("ffmpeg not found. Install it with: brew install ffmpeg")

    def decode(self, jpeg_ls: bytes) -> RawFrame:
        command = [
            self.ffmpeg_path,
            "-hide_banner",
            "-loglevel",
            "error",
            "-f",
            "jpegls_pipe",
            "-i",
            "pipe:0",
            "-f",
            "rawvideo",
            "-pix_fmt",
            "gray16le",
            "pipe:1",
        ]

        process = subprocess.run(
            command,
            input=jpeg_ls,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

        if process.returncode != 0:
            message = process.stderr.decode("utf-8", errors="replace")
            raise RuntimeError(message)

        raw_bytes = process.stdout
        pixel_count = len(raw_bytes) // 2

        common_sizes = [
            (384, 288),
            (320, 240),
            (640, 480),
            (160, 120),
            (80, 60),
        ]

        for width, height in common_sizes:
            if width * height == pixel_count:
                array = np.frombuffer(
                    raw_bytes,
                    dtype="<u2",
                ).reshape(height, width)

                return RawFrame(
                    width=width,
                    height=height,
                    data=array,
                )

        raise RuntimeError(f"Decoded frame has {pixel_count} pixels; unknown resolution.")