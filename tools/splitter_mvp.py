from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

import numpy as np
from PIL import Image

JST = timezone(timedelta(hours=9))


def load_rgba(path: Path) -> Image.Image:
    return Image.open(path).convert("RGBA")


def alpha_bbox(image: Image.Image):
    alpha = np.array(image.getchannel("A"))
    ys, xs = np.where(alpha > 0)
    if len(xs) == 0 or len(ys) == 0:
        return None
    return int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1


def trim_transparent(image: Image.Image) -> Image.Image:
    bbox = alpha_bbox(image)
    if bbox is None:
        raise ValueError("No visible pixels found.")
    return image.crop(bbox)


def fit_to_canvas(image: Image.Image, canvas_size: int) -> Image.Image:
    canvas = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    part = image
    max_side = max(part.size)
    if max_side > canvas_size:
        ratio = canvas_size / max_side
        part = part.resize((int(part.width * ratio), int(part.height * ratio)), Image.Resampling.LANCZOS)
    x = (canvas_size - part.width) // 2
    y = (canvas_size - part.height) // 2
    canvas.alpha_composite(part, (x, y))
    return canvas


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--out", type=Path, default=Path("assets/generated/test"))
    parser.add_argument("--canvas", type=int, default=2048)
    args = parser.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    image = load_rgba(args.input)
    trimmed = trim_transparent(image)
    canvas = fit_to_canvas(trimmed, args.canvas)

    stem = args.input.stem
    trimmed_name = f"{stem}_trimmed.png"
    canvas_name = f"{stem}_canvas_{args.canvas}.png"
    trimmed.save(args.out / trimmed_name)
    canvas.save(args.out / canvas_name)

    manifest = {
        "tool": "splitter_mvp.py",
        "character": "Mipurin",
        "generated_at": datetime.now(JST).isoformat(),
        "source": str(args.input),
        "canvas": {"width": args.canvas, "height": args.canvas},
        "files": [trimmed_name, canvas_name]
    }
    (args.out / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Done")


if __name__ == "__main__":
    main()
