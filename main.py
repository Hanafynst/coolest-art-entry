"""Emit the contest artwork: a colossal whale folded from white paper
drifting through early-morning haze, a bright vermilion sun disc behind
it and a still harbor spread out below.

The picture ships inside this repository as art.jpg. Running the program
copies those exact bytes to entry.png inside the chosen output folder,
so the produced file never changes between runs.
"""

import hashlib
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "art.jpg"
MAX_BYTES = 1_048_576
JPEG_MAGIC = b"\xff\xd8"


def load_source() -> bytes:
    if not SOURCE.is_file():
        raise FileNotFoundError(f"bundled artwork is missing: {SOURCE}")
    data = SOURCE.read_bytes()
    if not data.startswith(JPEG_MAGIC):
        raise ValueError("art.jpg does not start with the JPEG magic bytes ff d8")
    if len(data) > MAX_BYTES:
        raise ValueError(
            f"art.jpg weighs {len(data)} bytes, over the {MAX_BYTES} byte cap"
        )
    return data


def main() -> int:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"

    data = load_source()
    with open(target, "wb") as handle:
        handle.write(data)

    digest = hashlib.sha256(data).hexdigest()
    print(f"wrote {target} ({len(data)} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
