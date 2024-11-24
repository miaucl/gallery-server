"""Dither a image using a palette."""

import os
from typing import cast

from PIL import Image
from PIL.ImagePalette import ImagePalette

from gallery_server.const import PALETTES


def read_act_palette(act_file_path: str) -> list[tuple[int, int, int]]:
    """Read a .act file and returns a list of 256 RGB tuples.

    Parameters
    ----------
    act_file_path
        The path to the act palette

    Returns
    -------
    list
        The palette

    Raises
    ------
    ValueError
        When the palette does not contain valid data
    ReferenceError
        When the palette is not found

    """
    if not os.path.exists(act_file_path):
        raise ReferenceError(f"Palette not found: {act_file_path}")
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


def convert_image_to_bmp_with_palette(img: Image.Image, palette: str) -> Image.Image:
    """Convert an image to BMP format using a color table from a .act file.

    Parameters
    ----------
    img
        The image to convert
    palette
        The palette

    Returns
    -------
    ImageFile
        The converted image

    """
    # Read the ACT file palette
    palette_data = read_act_palette(os.path.join(PALETTES, f"{palette}.act"))

    # Create a new image with the palette
    palette_image = Image.new("P", (1, 1))
    palette_image.putpalette(cast(ImagePalette, palette_data))

    # Quantize the image to match the palette
    img = img.quantize(palette=palette_image)

    return img
