from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from PIL import Image

# make_face_crop_for_photoshop.py と同じ座標
CROP_BOX = (560, 360, 1490, 1160)
TARGET_W = CROP_BOX[2] - CROP_BOX[0]
TARGET_H = CROP_BOX[3] - CROP_BOX[1]


def remove_green_bg(img: Image.Image) -> Image.Image:
    img = img.convert("RGBA")
    arr = np.array(img).astype(np.uint8)

    r = arr[:, :, 0].astype(np.int16)
    g = arr[:, :, 1].astype(np.int16)
    b = arr[:, :, 2].astype(np.int16)

    # 明るい緑背景を透明化
    mask = (g > 150) & (g > r + 50) & (g > b + 50)

    arr[mask, 3] = 0

    return Image.fromarray(arr, "RGBA")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--base",
        type=Path,
        default=Path("assets/unity-ready/mipurin_default/base/mipurin_base_default.png"),
    )
    parser.add_argument(
        "--edited-crop",
        type=Path,
        required=True,
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("assets/unity-ready/mipurin_default/face_base"),
    )
    args = parser.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)

    base = Image.open(args.base).convert("RGBA")
    edited = Image.open(args.edited_crop).convert("RGBA")

    print(f"Base size: {base.size}")
    print(f"Edited crop size: {edited.size}")
    print(f"Target crop size: {(TARGET_W, TARGET_H)}")

    # まず緑背景を透明化
    edited_alpha = remove_green_bg(edited)

    # Photoshop側でサイズが変わるので、元のcropサイズへ戻す
    edited_alpha = edited_alpha.resize((TARGET_W, TARGET_H), Image.Resampling.LANCZOS)

    args.out_dir.mkdir(parents=True, exist_ok=True)

    crop_out = args.out_dir / "mipurin_face_base_crop.png"
    full_out = args.out_dir / "mipurin_face_base_fullcanvas.png"
    preview_out = args.out_dir / "preview_face_base_on_character.png"

    edited_alpha.save(crop_out)

    full = Image.new("RGBA", base.size, (0, 0, 0, 0))
    full.alpha_composite(edited_alpha, (CROP_BOX[0], CROP_BOX[1]))
    full.save(full_out)

    preview = base.copy()
    preview.alpha_composite(full)
    preview.save(preview_out)

    print("Done")
    print(crop_out)
    print(full_out)
    print(preview_out)


if __name__ == "__main__":
    main()
