# core/ocr_engine.py

import os
from typing import List, Dict
from paddleocr import PaddleOCR
import cv2


class OCREngine:
    """
    OCR Engine wrapper.
    Responsible ONLY for text extraction.
    """

    def __init__(self, lang: str = "en"):
        self.ocr = PaddleOCR(
            use_angle_cls=True,
            lang=lang,
          
        )

    def run_ocr(self, page_entries: List[Dict]) -> List[Dict]:
        """
        Runs OCR on page images.

        Args:
            page_entries: Output from pdf_loader

        Returns:
            OCR results per page
        """

        ocr_results = []

        for page in page_entries:
            image_path = page["image_path"]
            page_number = page["page"]

            if not os.path.exists(image_path):
                continue

            image = cv2.imread(image_path)
            height, width = image.shape[:2]

            result = self.ocr.ocr(image_path, cls=True)

            blocks = []

            for line in result[0]:
                bbox_points = line[0]
                text = line[1][0]
                confidence = float(line[1][1])

                xs = [p[0] for p in bbox_points]
                ys = [p[1] for p in bbox_points]

                bbox = [
                    int(min(xs)),
                    int(min(ys)),
                    int(max(xs)),
                    int(max(ys))
                ]

                blocks.append({
                    "text": text,
                    "bbox": bbox,
                    "confidence": confidence
                })

            ocr_results.append({
                "page": page_number,
                "width": width,
                "height": height,
                "blocks": blocks
            })

        return ocr_results
