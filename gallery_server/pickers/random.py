"""Pick a random image."""

import os
import random

from gallery_server.const import MEDIA


def pick_random_image_by_seed(
    seed: str | None = None,
    allowed_extensions: list[str] = [".png", ".jpg", ".jpeg", ".bmp", ".gif"],
):
    """Pick an image from the folder based on the seed.

    Parameters
    ----------
    seed
        The seed for the randomizer
    allowed_extensions
        A list of allowed extensions

    Returns
    -------
    str
        Full path to the selected image or a message if no images are found.

    Raises
    ------
    ReferenceError
        If no image is present

    """
    # List all files in the folder
    all_files = os.listdir(MEDIA)
    # Filter for image files (e.g., jpg, png, bmp)
    image_files = [
        f for f in all_files if f.lower().endswith(tuple(allowed_extensions))
    ]

    if not image_files:
        raise ReferenceError(
            f"No images found in the folder for following extensions: {allowed_extensions}."
        )

    # Set the seed
    random.seed(seed)

    # Select an image
    selected_image = random.choice(image_files)
    return os.path.join(MEDIA, selected_image)
