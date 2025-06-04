import io
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pdf_utils import images_to_pdf
from PIL import Image
from pdf2image import convert_from_bytes


def create_sample_images(count):
    images = []
    for i in range(count):
        img = Image.new("RGB", (10, 10), color=(i * 20 % 255, i * 30 % 255, i * 40 % 255))
        images.append(img)
    return images


def test_pdf_page_count(tmp_path):
    imgs = create_sample_images(3)
    pdf_bytes = images_to_pdf(imgs)

    # write to tmp file
    pdf_path = tmp_path / "output.pdf"
    pdf_path.write_bytes(pdf_bytes)

    pages = convert_from_bytes(pdf_bytes)
    assert len(pages) == 3
