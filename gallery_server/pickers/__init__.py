"""A collection image pickers using different algorithms."""

from .power_law import pick_weighted_image_by_power_law_by_seed
from .random import pick_random_image_by_seed

__all__ = ["pick_random_image_by_seed", "pick_weighted_image_by_power_law_by_seed"]


def pick_image_by_method(method: str, **kwargs) -> str:
    """Pick an image using the specified method."""
    if method == "random":
        return pick_random_image_by_seed(**kwargs)
    elif method == "power-law":
        return pick_weighted_image_by_power_law_by_seed(**kwargs)
    else:
        raise ValueError("Unknown picker method: %s", method)
