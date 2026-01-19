# core/pdf_loader.py

import os
import sys
from typing import List, Dict
from pdf2image import convert_from_path


PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)


def load_pdf(
    pdf_path: str,
    output_dir: str = None,
    dpi: int = 300
) -> List[Dict]:

    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    if output_dir is None:
        output_dir = os.path.join(PROJECT_ROOT, "output", "pages")

    os.makedirs(output_dir, exist_ok=True)

    pages = convert_from_path(pdf_path, dpi=dpi)

    page_entries = []

    for idx, page in enumerate(pages, start=1):
        image_name = f"page_{idx}.png"
        image_path = os.path.join(output_dir, image_name)

        page.save(image_path, "PNG")

        page_entries.append({
            "page": idx,
            "image_path": os.path.abspath(image_path)
        })

    return page_entries


