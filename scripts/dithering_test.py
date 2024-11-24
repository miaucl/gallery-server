"""Dithering test script."""
import os

from PIL import Image

script_dir = os.path.dirname(os.path.realpath(__file__))


def read_act_palette(act_file_path):
    """Read a .act file and returns a list of 256 RGB tuples."""
    with open(act_file_path, "rb") as f:
        data = f.read()
    if len(data) < 768:
        raise ValueError("ACT file does not contain a full 256-color palette.")
    palette = []
    for i in range(256):
        r = data[i * 3]
        g = data[i * 3 + 1]
        b = data[i * 3 + 2]
        palette.extend([r, g, b])
    return palette


def convert_image_to_bmp_with_palette(image_path, act_file_path, output_path):
    """Convert an image to BMP format using a color table from a .act file."""
    # Read the ACT file palette
    palette = read_act_palette(act_file_path)

    # Open the source image
    img = Image.open(image_path).convert("RGB")

    # Create a new image with the palette
    palette_image = Image.new("P", (1, 1))
    palette_image.putpalette(palette)

    # Quantize the image to match the palette
    img = img.quantize(palette=palette_image)

    # Save as BMP
    img.save(output_path, format="BMP")
    print(f"Image saved to {output_path}")


all_files = os.listdir(os.path.join(script_dir, "..", "media"))
print(all_files)
image_files = [
    f
    for f in all_files
    if f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif"))
]
for image_file in image_files:
    convert_image_to_bmp_with_palette(
        image_path=os.path.join(script_dir, "..", "media", image_file),
        act_file_path=os.path.join(
            script_dir, "..", "assets", "palettes", "6-color.act"
        ),  # Path to the .act file
        output_path=os.path.join(
            script_dir,
            "..",
            "out",
            f"{os.path.splitext(os.path.basename(image_file))[0]}.bmp",
        ),  # Output BMP file
    )
