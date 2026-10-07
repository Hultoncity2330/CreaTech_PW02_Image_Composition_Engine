import numpy as np
from PIL import Image, UnidentifiedImageError


def load_image(path: str) -> np.ndarray:
    """Load an image as an RGB NumPy array with values between 0 and 1."""
    try:
        image = Image.open(path).convert("RGB")
    except FileNotFoundError:
        raise FileNotFoundError(f"Image not found: {path}")
    except UnidentifiedImageError:
        raise ValueError(f"Unreadable image: {path}")

    return np.array(image) / 255


def array_to_image(image: np.ndarray) -> Image.Image:
    """Convert a NumPy image array to a Pillow image."""
    adjusted = np.array(
        np.clip(image, 0, 1) * 255,
        dtype = np.uint8,
    )

    return Image.fromarray(adjusted)


def save_image(image: np.ndarray, path: str) -> None:
    """Save a NumPy image array to a file."""
    pil_image = array_to_image(image)

    try:
        pil_image.save(path)
    except OSError as error:
        raise OSError(f"Could not save image to: {path}") from error

