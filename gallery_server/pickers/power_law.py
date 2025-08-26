"""Pick a random image."""

from datetime import datetime
import math
import os
import platform
import random

from gallery_server.const import MEDIA


def _power_for_decay(days_old: int, fraction: float) -> float:
    """Calculate power for a power-law decay such that after `days_old` days, weight is `fraction` of today's weight.

    How it works:

    days = 0 → weight = 1
    days = 365 → weight ≈ 0.1
    You can adjust the “10” to any fraction (e.g., 0.05 → weight of 1/20 after a year)

    ```
    # Example: 1 year old = 1/10 of today's weight
    p = power_for_decay(365, 0.1)
    print("Power factor:", p)
    ```


    Parameters
    ----------
    days_old: int
        The number of days old the item is.
    fraction: float
        The fraction of today's weight the item should have after `days_old` days.

    Returns
    -------
    float
        The power to apply for the decay.

    """
    return math.log(1 / fraction) / math.log(1 + days_old)


def _get_creation_time(path: str) -> datetime:
    """Return the creation time of a file as datetime. Tries to get true creation time if possible, falls back to mtime.

    Parameters
    ----------
    path: str
        The path to the file.

    Returns
    -------
    datetime
        The creation time of the file.

    """
    if platform.system() == "Windows":
        # Windows
        return datetime.fromtimestamp(os.path.getctime(path))
    else:
        # Linux and macOS: try st_birthtime, fallback to mtime
        stat = os.stat(path)
        if hasattr(stat, "st_birthtime"):
            return datetime.fromtimestamp(stat.st_birthtime)
        else:
            # fallback: last modification time
            return datetime.fromtimestamp(stat.st_mtime)


def pick_weighted_image_by_power_law_by_seed(
    power: float = 0.25,
    seed: str | None = None,
    allowed_extensions: list[str] = [".png", ".jpg", ".jpeg", ".bmp", ".gif"],
):
    """Pick a weighted image from the folder based on the seed and power.

    Parameters
    ----------
    power
        The power to apply to the image selection
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

    now = datetime.now()

    days_since_list = []

    for fpath in all_files:
        days_since_list.append(
            (now - _get_creation_time(os.path.join(MEDIA, fpath))).days
        )

    # Compute weights using power-law decay
    weights = [(1 / (1 + days)) ** power for days in days_since_list]

    # Normalize weights
    total = sum(weights)
    weights = [w / total for w in weights]

    # Set the seed
    random.seed(seed)

    # Select an image
    selected_image = random.choices(all_files, weights=weights, k=1)[0]
    return os.path.join(MEDIA, selected_image)
