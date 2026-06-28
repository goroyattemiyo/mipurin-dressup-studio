from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw


DEFAULT_CROP_BOX = (560, 360, 1490, 1160)
DEFAULT_FACE_MASK_BOX_ABS = (760, 640, 1290, 1030)
GREEN = (0, 255, 0, 255)


def composite_on_green(img: Image.Image) -> Image.Image:
    img = img.convert("RGBA")
    bg = Image.new("RGBA", img.size, GREEN)
    bg.alpha_composite(img)
    return bg.convert("RGB")


def draw_guide(base: Image.Image, crop_box, face_mask_box_abs, out_path: Path) -> None:
    guide = base.convert("RGBA").copy()
    draw = ImageDraw.Draw(guide)

    draw.rectangle(crop_box, outline=(255, 0, 0, 255), width=6)
    draw.ellipse(face_mask_box_abs, outline=(0, 160, 255, 255), width=6)

    # Rough eye and mouth guide boxes.
    draw.rectangle((790, 735, 1010, 890), outline=(255, 200, 0, 255), width=4)
    draw.rectangle((1040, 735, 1260, 890), outline=(255, 200, 0, 255), width=4)
    draw.rectangle((955, 885, 1100, 980), outline=(255, 80, 200, 255), width=4)

    guide.save(out_path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("assets/unity-ready/mipurin_default/base/mipurin_base_default.png"),
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("assets/work/face_edit"),
    )
    args = parser.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)

    base = Image.open(args.input).convert("RGBA")
    crop_box = DEFAULT_CROP_BOX
    face_mask_box_abs = DEFAULT_FACE_MASK_BOX_ABS

    face_crop = base.crop(crop_box)
    face_crop.save(args.out_dir / "face_crop_transparent.png")

    face_crop_green = composite_on_green(face_crop)
    face_crop_green.save(args.out_dir / "face_crop_for_photoshop_green_bg.png")

    draw_guide(
        base,
        crop_box,
        face_mask_box_abs,
        args.out_dir / "full_canvas_face_guide.png",
    )

    crop_x1, crop_y1, _, _ = crop_box
    rel_face_mask_box = (
        face_mask_box_abs[0] - crop_x1,
        face_mask_box_abs[1] - crop_y1,
        face_mask_box_abs[2] - crop_x1,
        face_mask_box_abs[3] - crop_y1,
    )

    crop_guide = face_crop_green.convert("RGBA")
    draw = ImageDraw.Draw(crop_guide)
    draw.ellipse(rel_face_mask_box, outline=(0, 160, 255, 255), width=5)
    draw.rectangle((230, 375, 450, 530), outline=(255, 200, 0, 255), width=4)
    draw.rectangle((480, 375, 700, 530), outline=(255, 200, 0, 255), width=4)
    draw.rectangle((395, 525, 540, 620), outline=(255, 80, 200, 255), width=4)
    crop_guide.save(args.out_dir / "face_crop_guide.png")

    info = {
        "source": str(args.input),
        "crop_box": crop_box,
        "face_mask_box_abs": face_mask_box_abs,
        "face_mask_box_in_crop": rel_face_mask_box,
        "files": {
            "transparent_crop": "face_crop_transparent.png",
            "photoshop_input": "face_crop_for_photoshop_green_bg.png",
            "crop_guide": "face_crop_guide.png",
            "full_guide": "full_canvas_face_guide.png"
        }
    }

    (args.out_dir / "face_crop_info.json").write_text(
        json.dumps(info, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("Done")
    print(args.out_dir)


if __name__ == "__main__":
    main()
