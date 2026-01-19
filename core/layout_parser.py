# core/layout_parser.py

from typing import List, Dict


class LayoutParser:
    """
    Organizes OCR blocks into lines and page regions.
    No business logic here.
    """

    def __init__(self, y_tolerance: int = 15):
        self.y_tolerance = y_tolerance

    def group_blocks_into_lines(self, blocks: List[Dict]) -> List[Dict]:
        """
        Groups OCR blocks into text lines using Y-axis proximity.
        """

        sorted_blocks = sorted(blocks, key=lambda b: (b["bbox"][1], b["bbox"][0]))
        lines = []

        for block in sorted_blocks:
            placed = False
            x1, y1, x2, y2 = block["bbox"]
            y_center = (y1 + y2) // 2

            for line in lines:
                ly1, ly2 = line["bbox"][1], line["bbox"][3]
                l_center = (ly1 + ly2) // 2

                if abs(y_center - l_center) <= self.y_tolerance:
                    line["tokens"].append(block)
                    line["bbox"] = [
                        min(line["bbox"][0], x1),
                        min(line["bbox"][1], y1),
                        max(line["bbox"][2], x2),
                        max(line["bbox"][3], y2)
                    ]
                    placed = True
                    break

            if not placed:
                lines.append({
                    "tokens": [block],
                    "bbox": block["bbox"].copy()
                })

        # Sort tokens inside each line left → right
        for line in lines:
            line["tokens"].sort(key=lambda t: t["bbox"][0])
            line["text"] = " ".join(t["text"] for t in line["tokens"])

        return lines

    def split_regions(self, lines: List[Dict], page_height: int) -> Dict[str, List[Dict]]:
        """
        Splits lines into header, body, footer regions.
        """

        header_limit = int(page_height * 0.25)
        footer_limit = int(page_height * 0.85)

        regions = {
            "header": [],
            "body": [],
            "footer": []
        }

        for line in lines:
            y1 = line["bbox"][1]

            if y1 <= header_limit:
                regions["header"].append(line)
            elif y1 >= footer_limit:
                regions["footer"].append(line)
            else:
                regions["body"].append(line)

        return regions

    def parse_page(self, ocr_page: Dict) -> Dict:
        """
        Full layout parsing for a page.
        """

        lines = self.group_blocks_into_lines(ocr_page["blocks"])
        regions = self.split_regions(lines, ocr_page["height"])

        return {
            "page": ocr_page["page"],
            "lines": lines,
            "regions": regions
        }

    def parse_document(self, ocr_results: List[Dict]) -> List[Dict]:
        """
        Parses all pages in a document.
        """

        parsed_pages = []

        for page in ocr_results:
            parsed_pages.append(self.parse_page(page))

        return parsed_pages
