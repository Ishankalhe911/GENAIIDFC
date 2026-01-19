from core.pdf_loader import load_pdf
from core.ocr_engine import OCREngine
from core.layout_parser import LayoutParser

pages = load_pdf("C:/Users/admin/Downloads/172561841_pg1.pdf")
ocr = OCREngine()
ocr_out = ocr.run_ocr(pages)

parser = LayoutParser()
parsed = parser.parse_document(ocr_out)

print(parsed[0]["regions"].keys())
print(parsed[0]["lines"][:3])
