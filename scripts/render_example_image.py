"""
Generate an example image rendered with the 5x7 PIL bitmap font.

Loads the generated font5x7 font and renders sample text to a PNG,
scaling up the result for visibility.
"""

import pathlib
from PIL import Image, ImageDraw, ImageFont

def _get_text_size(font: ImageFont.ImageFont, text: str) -> tuple[int, int]:
    """Get the size of the text when rendered with the given font."""

    # PIL's ImageFont does not have a getsize method for bitmap fonts,
    # so we create a dummy image to measure the text size.
    dummy_img = Image.new("RGB", (1, 1))
    draw = ImageDraw.Draw(dummy_img)

    x0, y0, x1, y1 = draw.textbbox((0, 0), text, font=font)
    return (x1 - x0, y1 - y0)

def render_example_image(
        font_path: pathlib.Path,
        output_path: pathlib.Path,
        *,
        text: str = "Hello, World!",
        margin: int = 2,
        scale: int = 4,
        text_color: tuple[int, int, int] = (255, 255, 255),
        background_color: tuple[int, int, int] = (0, 0, 0),
    ) -> None:

    # Load the PIL font
    font = ImageFont.load(str(font_path))

    # Create an image
    text_size = _get_text_size(font, text)
    img_size = (text_size[0] + 2 * margin, text_size[1] + 2 * margin)
    img = Image.new("RGB", img_size, color=background_color)

    # Draw some text using the loaded font
    draw = ImageDraw.Draw(img)
    draw.text((margin, margin), text, font=font, fill=text_color)

    # Resize the image to make it more visible
    new_size = (img.width * scale, img.height * scale)
    img_resized = img.resize(new_size, resample=Image.NEAREST)

    # Save the image
    img_resized.save(output_path)
    print(f"Saved: {output_path}")

if __name__ == "__main__":
    project_root = pathlib.Path(__file__).parent.parent
    font_path = project_root / "fonts" / "font5x7.pil"
    output_path = project_root / "images" / "example.png"
    text = "Hello, World!\n" \
        "This is a test of the 5x7 font.\n" \
        "0123456789\n" \
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ\n" \
        "abcdefghijklmnopqrstuvwxyz\n" \
        "!@#$%^&*()_+-=[]{}|;':\",./<>?\n" \
        "¡¢£¤¥¦°´¶«»¿ß±·×÷µ²³¼½"
    render_example_image(font_path, output_path, text=text)
