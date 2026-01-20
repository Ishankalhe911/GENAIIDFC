from core.pdf_loader import load_pdf
from core.ocr_engine import OCREngine
from core.layout_parser import LayoutParser
from core.confidence import ConfidenceScorer
from core.validator import OutputValidator


import time


def main():
    pdf_path = "sample.pdf"  # change as needed

    print("[1] Loading PDF...")
    pages = load_pdf(pdf_path)

    print("[2] Running OCR...")
    ocr = OCREngine()
    ocr_output = ocr.run_ocr(pages)

    print("[3] Parsing Layout...")
    parser = LayoutParser()
    parsed_pages = parser.parse_document(ocr_output)

    # Safely print regions for the first page
    if parsed_pages:
     print("Regions detected:", parsed_pages[0]["regions"].keys())
     # Optionally show first few lines of text
     print("First 3 lines:", [line["text"] for line in parsed_pages[0]["lines"][:3]])
    else:
     print("No pages parsed.")


    

    print("[4] Computing Confidence...")
    conf = ConfidenceScorer()
    dealer_conf = conf.dealer_name_confidence(0.91, region="header")
    hp_conf = conf.numeric_confidence(True)

    doc_conf = conf.document_confidence([
        dealer_conf,
        hp_conf,
        1.0,  # stamp absent
        0.85  # signature
    ])

    print("Document confidence:", doc_conf)

    print("[5] Validating Schema...")
    raw_output = {
        "doc_id": "test_doc",
        "fields": {
            "dealer_name": "ABC Tractors",
            "model_name": "Mahindra 575 DI",
            "horse_power": 50,
            "asset_cost": 525000,
            "signature": {"present": True, "bbox": [10, 20, 100, 200]},
            "stamp": {"present": False, "bbox": None}
        },
        "confidence": doc_conf,
        "processing_time_sec": 3.2,
        "cost_estimate_usd": 0.002
    }

    validator = OutputValidator()
    final_output = validator.validate(raw_output)


    print("\nFinal Validated Output:")
    print(final_output)


if __name__ == "__main__":
    main()
