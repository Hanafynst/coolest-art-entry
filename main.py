"""Write our picture to /output/entry.png.

The picture is a generated image: a monumental origami crane of dull
cracked paper standing in a rain-wet futuristic megacity intersection
at night, brilliant white light glowing from the cracks in the paper,
wet asphalt reflections, one bold silhouette. The program only copies
the bundled image, so every run writes the same bytes.
"""

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "art.jpg"
MAX_BYTES = 1_048_576
OUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def main() -> None:
    data = SOURCE.read_bytes()
    if not data.startswith(b"\xff\xd8"):
        found = data[:2].hex() if data else "empty file"
        raise ValueError(f"art.jpg is not a JPEG image: expected magic bytes ffd8, found {found}")
    if len(data) > MAX_BYTES:
        raise ValueError(f"art.jpg is {len(data)} bytes, over the {MAX_BYTES} byte limit")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / "entry.png"
    shutil.copyfile(SOURCE, out)
    print(f"wrote {out} ({len(data)} bytes)")


if __name__ == "__main__":
    main()
