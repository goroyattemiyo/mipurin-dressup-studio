from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter


LEFT_EYE_BOX = (835, 755, 1000, 895)
RIGHT_EYE_BOX = (1050, 755, 1215, 895)
MOUTH_BOX = (985, 890, 1080, 960)


def color_mask_eye(source: Image.Image, box) -> Image.Image:
    source = source.convert("RGBA")
    arr = np.array(source)
    h, w = arr.shape[:2]

    mask = np.zeros((h, w), dtype=np.uint8)

    x1, y1, x2, y2 = box
    region = arr[y1:y2, x1:x2]

    r = region[:, :, 0].astype(np.int16)
    g = region[:, :, 1].astype(np.int16)
    b = region[:, :, 2].astype(np.int16)
    a = region[:, :, 3]

    dark = (r < 135) & (g < 105) & (b < 95)
    brown_iris = (r > 70) & (r < 230) & (g > 35) & (g < 170) & (b < 120) & (r > b + 25)
    white_highlight = (r > 210) & (g > 200) & (b > 185)
    orange_eye = (r > 150) & (g > 75) & (g < 190) & (b < 120) & (r > g + 10)

    local = (dark | brown_iris | white_highlight | orange_eye) & (a > 0)

    mask[y1:y2, x1:x2] = np.where(local, 255, 0).astype(np.uint8)

    mask_img = Image.fromarray(mask, "L")
    mask_img = mask_img.filter(ImageFilter.MaxFilter(3))
    mask_img = mask_img.filter(ImageFilter.GaussianBlur(0.35))

    out = Image.new("RGBA", source.size, (0, 0, 0, 0))
    out.paste(source, (0, 0), mask_img)
    return out


def color_mask_mouth(source: Image.Image, box) -> Image.Image:
    source = source.convert("RGBA")
    arr = np.array(source)
    h, w = arr.shape[:2]

    mask = np.zeros((h, w), dtype=np.uint8)

    x1, y1, x2, y2 = box
    region = arr[y1:y2, x1:x2]

    r = region[:, :, 0].astype(np.int16)
    g = region[:, :, 1].astype(np.int16)
    b = region[:, :, 2].astype(np.int16)
    a = region[:, :, 3]

    red_lip = (r > 145) & (g < 145) & (b < 135) & (r > g + 25)
    dark_line = (r < 150) & (g < 100) & (b < 90)
    inner_shadow = (r > 80) & (r < 190) & (g < 110) & (b < 110)

    local = (red_lip | dark_line | inner_shadow) & (a > 0)

    mask[y1:y2, x1:x2] = np.where(local, 255, 0).astype(np.uint8)

    mask_img = Image.fromarray(mask, "L")
    mask_img = mask_img.filter(ImageFilter.MaxFilter(3))
    mask_img = mask_img.filter(ImageFilter.GaussianBlur(0.35))

    out = Image.new("RGBA", source.size, (0, 0, 0, 0))
    out.paste(source, (0, 0), mask_img)
    return out


def combine_layers(size, layers):
    out = Image.new("RGBA", size, (0, 0, 0, 0))
    for layer in layers:
        out.alpha_composite(layer.convert("RGBA"))
    return out


def scale_alpha_part(part: Image.Image, box, scale: float) -> Image.Image:
    part = part.convert("RGBA")
    x1, y1, x2, y2 = box
    region = part.crop(box)

    new_w = max(1, int(region.width * scale))
    new_h = max(1, int(region.height * scale))
    region = region.resize((new_w, new_h), Image.Resampling.LANCZOS)

    cx = (x1 + x2) // 2
    cy = (y1 + y2) // 2

    out = Image.new("RGBA", part.size, (0, 0, 0, 0))
    out.alpha_composite(region, (cx - new_w // 2, cy - new_h // 2))
    return out


def preview(base: Image.Image, layers) -> Image.Image:
    p = base.convert("RGBA").copy()
    for layer in layers:
        p.alpha_composite(layer.convert("RGBA"))
    return p


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--original",
        type=Path,
        default=Path("assets/unity-ready/mipurin_default/base/mipurin_base_default.png"),
    )
    parser.add_argument(
        "--no-face",
        type=Path,
        default=Path("assets/unity-ready/mipurin_default/base/mipurin_base_no_face.png"),
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("assets/unity-ready/mipurin_default/face_parts"),
    )
    args = parser.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)

    original = Image.open(args.original).convert("RGBA")
    no_face = Image.open(args.no_face).convert("RGBA")

    left_eye = color_mask_eye(original, LEFT_EYE_BOX)
    right_eye = color_mask_eye(original, RIGHT_EYE_BOX)
    eyes_open = combine_layers(original.size, [left_eye, right_eye])

    lip_open = color_mask_mouth(original, MOUTH_BOX)
    lip_small = scale_alpha_part(lip_open, MOUTH_BOX, 0.68)
    lip_close = Image.new("RGBA", original.size, (0, 0, 0, 0))

    eyes_open.save(args.out_dir / "mipurin_eyes_open.png")
    lip_open.save(args.out_dir / "mipurin_lip_sync_open.png")
    lip_small.save(args.out_dir / "mipurin_lip_sync_small.png")
    lip_close.save(args.out_dir / "mipurin_lip_sync_close.png")

    preview(no_face, [eyes_open, lip_open]).save(args.out_dir / "preview_eyes_open_lip_open.png")
    preview(no_face, [eyes_open, lip_small]).save(args.out_dir / "preview_eyes_open_lip_small.png")
    preview(no_face, [eyes_open, lip_close]).save(args.out_dir / "preview_eyes_open_lip_close.png")

    print("Done")
    print(args.out_dir)


if __name__ == "__main__":
    main()
