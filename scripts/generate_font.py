"""
Generate PIL-format font files from a 5x7 bitmap font source PNG.

Reads glyphs from the source image (font5x7_src.png) and outputs
a .pil (metrics) and .pbm (bitmap) file compatible with PIL/Pillow.
"""

import pathlib
import struct
from PIL import Image

SUPPORTED_CHARACTERS = [
    *(range(32, 127)),  # Printable ASCII
    0xA0,  # Non-breaking space
    0xA1,  # Inverted exclamation mark
    0xA2,  # Cent sign
    0xA3,  # Pound sign
    0xA4,  # Currency sign
    0xA5,  # Yen sign
    0xA6,  # Broken bar
    0xAB,  # Left-pointing double angle quotation mark
    0xAC,  # Not sign
    0xAD,  # Soft hyphen
    0xB0,  # Degree sign
    0xB1,  # Plus-minus sign
    0xB2,  # Superscript two
    0xB3,  # Superscript three
    0xB4,  # Acute accent
    0xB5,  # Micro sign
    0xB6,  # Pilcrow sign
    0xB7,  # Middle dot
    0xBB,  # Right-pointing double angle quotation mark
    0xBC,  # Vulgar fraction one quarter
    0xBD,  # Vulgar fraction one half
    0xBF,  # Inverted question mark
    0xD7,  # Multiplication sign
    0xDF,  # Latin small letter sharp s
    0xF7,  # Division sign
]

def create_pil_font(
    source_png: pathlib.Path,
    output_path: pathlib.Path,
    char_width: int = 5,
    char_height: int = 7,
    margin: int = 1,
    grid_cols: int = 16,
    advance_x: int = 6,
):
    src = Image.open(source_png).convert("1")  # Read as monochrome
    num_chars = 256
    out_w = num_chars * char_width
    out_h = char_height
    out_bitmap = Image.new("L", (out_w, out_h), 0)
    cell_w = char_width + margin
    cell_h = char_height + margin
    metrics = [None] * 256

    for code in SUPPORTED_CHARACTERS:
        col = code % grid_cols
        row = code // grid_cols
        sx = col * cell_w + margin
        sy = row * cell_h + margin
        glyph = src.crop((sx, sy, sx + char_width, sy + char_height))

        # paste glyph into output bitmap
        ox = code * char_width
        out_bitmap.paste(glyph, (ox, 0))

        # metrics
        # (dx, dy): advance from pen position after drawing this character
        # dst: drawing destination box (relative coordinates from pen position)
        # src: glyph position on the output bitmap
        dx, dy = advance_x, 0
        dst = (0, 0, char_width, char_height)
        src_box = (ox, 0, ox + char_width, char_height)
        metrics[code] = (dx, dy) + dst + src_box

    # save the bitmap as .pbm
    out_bitmap.save(output_path.with_suffix(".pbm"))

    # save the metrics as .pil
    with open(output_path.with_suffix(".pil"), "wb") as fp:
        fp.write(b"PILfont\n")
        fp.write(f";;;;;;{char_height};\n".encode("ascii"))
        fp.write(b"DATA\n")

        for m in metrics:
            if m is None:
                m = (0,) * 10
            for v in m:
                if v < 0:
                    v += 65536
                fp.write(struct.pack(">H", v))

    print(f"Saved: {output_path}.pil / {output_path}.pbm")


if __name__ == "__main__":
    project_root = pathlib.Path(__file__).parent.parent
    source_path = project_root / "src" / "font5x7_src.png"
    output_path = project_root / "fonts" / "font5x7"
    create_pil_font(
        source_png=source_path,
        output_path=output_path,
    )
