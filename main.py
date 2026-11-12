"""Emit the entry artwork for make.fun's "Make the coolest art".

The picture shows a huge dragon folded from deep crimson paper,
sweeping in a long curve above a night market strung with glowing
lanterns, drawn in a bold graphic-novel style while tiny crowd
silhouettes look up from the stalls below. This program simply
copies the bundled JPEG to the output location, so the bytes it
produces never change from run to run.
"""

import hashlib
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
IMAGE = HERE / "art.jpg"
SIZE_LIMIT = 1_048_576


def target_dir() -> Path:
    return Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def main() -> None:
    payload = IMAGE.read_bytes()
    if payload[:2] != b"\xff\xd8":
        raise ValueError("art.jpg lacks JPEG magic bytes ff d8; refusing to emit it")
    if len(payload) > SIZE_LIMIT:
        raise ValueError(f"art.jpg is {len(payload)} bytes, above the {SIZE_LIMIT} byte cap")
    out_dir = target_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / "entry.png"
    shutil.copyfile(IMAGE, dest)
    digest = hashlib.sha256(dest.read_bytes()).hexdigest()
    print(f"wrote {dest} ({len(payload)} bytes, sha256 {digest})")


if __name__ == "__main__":
    main()
