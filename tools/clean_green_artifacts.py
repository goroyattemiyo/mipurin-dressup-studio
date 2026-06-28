from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from PIL import Image


def remove_green_pixels(path: Path, out_path: Path) -> None:
    img = Image.open(path).convert("RGBA")
    arr = np.array(img)

    r = arr[:, :, 0].astype(np.int16)
    g = arr[:, :, 1].astype(np.int16)
    b = arr[:, :, 2].astype(np.int16)
    a = arr[:, :, 3]

    green = (a > 0) & (g > 140) & (g > r + 45) & (g > b + 45)
    arr[green, 3] = 0

    out_path.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(arr, "RGBA").save(out_path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("targets", nargs="+", type=Path)
    args = parser.parse_args()

    for path in args.targets:
        remove_green_pixels(path, path)
        print(f"cleaned: {path}")


if __name__ == "__main__":
    main()
