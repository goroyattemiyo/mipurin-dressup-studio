from __future__ import annotations

import argparse
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image


def is_background(pixel, threshold: int) -> bool:
    r, g, b, a = pixel
    return a > 0 and r >= threshold and g >= threshold and b >= threshold


def remove_edge_white_background(image: Image.Image, threshold: int) -> Image.Image:
    image = image.convert("RGBA")
    arr = np.array(image)
    h, w, _ = arr.shape

    visited = np.zeros((h, w), dtype=bool)
    remove = np.zeros((h, w), dtype=bool)
    q = deque()

    def add_if_bg(x: int, y: int):
        if x < 0 or y < 0 or x >= w or y >= h:
            return
        if visited[y, x]:
            return
        visited[y, x] = True
        if is_background(arr[y, x], threshold):
            remove[y, x] = True
            q.append((x, y))

    for x in range(w):
        add_if_bg(x, 0)
        add_if_bg(x, h - 1)

    for y in range(h):
        add_if_bg(0, y)
        add_if_bg(w - 1, y)

    while q:
        x, y = q.popleft()
        add_if_bg(x + 1, y)
        add_if_bg(x - 1, y)
        add_if_bg(x, y + 1)
        add_if_bg(x, y - 1)

    arr[remove, 3] = 0

    return Image.fromarray(arr, "RGBA")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--threshold", type=int, default=245)
    args = parser.parse_args()

    img = Image.open(args.input)
    out = remove_edge_white_background(img, args.threshold)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    out.save(args.out)

    print("Done")
    print(args.out)


if __name__ == "__main__":
    main()
