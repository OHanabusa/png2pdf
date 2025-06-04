import io
from typing import List
from PIL import Image


def images_to_pdf(images: List[Image.Image]) -> bytes:
    """Convert a list of PIL Images to PDF bytes."""
    if not images:
        raise ValueError("No images provided")
    rgb_images = [img.convert("RGB") for img in images]
    with io.BytesIO() as buf:
        rgb_images[0].save(
            buf,
            format="PDF",
            save_all=True,
            append_images=rgb_images[1:],
        )
        return buf.getvalue()
