# Intelligent Document AI for Invoice Field Extraction  
**IDFC – GenAI Hackathon (Convolve 4.0)**

---

## 1. Problem Overview

Financial institutions process large volumes of semi-structured documents such as invoices and quotations.  
Manual data entry is slow, error-prone, and expensive.

This project builds an **end-to-end Document AI pipeline** that extracts critical fields from invoice-type documents (tractor loan quotations as a reference use-case) under **real-world constraints**:
- No pre-labelled ground truth
- Multi-language documents (English, Hindi, Gujarati)
- Scanned, photographed, and handwritten inputs
- Strict cost and latency requirements

The system is designed to **generalize across invoice layouts** while maintaining high document-level accuracy.

---

## 2. Target Fields & Output Contract

For each input document (PDF), the system extracts:

| Field | Type | Matching Rule |
|------|------|---------------|
| Dealer Name | Text | Fuzzy match (≥90%) |
| Model Name | Text | Exact match |
| Horse Power | Numeric | Exact |
| Asset Cost | Numeric | Exact |
| Dealer Signature | Binary + Bounding Box | IoU ≥ 0.5 |
| Dealer Stamp | Binary + Bounding Box | IoU ≥ 0.5 |

Each document always produces a **complete JSON output**, even when fields are missing or unclear.

---

## 3. System Design Philosophy

This solution prioritizes **engineering intelligence over heavy model training**.

Key principles:
- **Schema-first design**: output structure never breaks
- **Fail-soft behavior**: no crashes, graceful degradation
- **Explainability**: every decision is auditable
- **Low-cost inference**: CPU-friendly, open-source components
- **Confidence-aware outputs**: extraction quality is quantified

---

## 4. High-Level Architecture

```

PDF Input
└── Image Conversion
└── OCR (text + bounding boxes)
├── Rule-Based Field Extractors
│     ├── Dealer Name (fuzzy + lookup)
│     ├── Model Name (exact lookup)
│     ├── Horse Power (regex + validation)
│     └── Asset Cost (numeric + context)
├── Vision Detectors
│     ├── Dealer Signature
│     └── Dealer Stamp
├── Validation & Self-Consistency Checks
└── Confidence Aggregation
↓
Structured JSON Output

```

---

## 5. Document Ingestion & OCR

- Input: PDF documents
- Conversion: PDF → Images
- OCR Engine: PaddleOCR / equivalent multilingual OCR
- Extracted:
  - Text
  - Bounding boxes
  - OCR confidence scores

OCR output acts as the **single source of truth** for downstream extraction.

---

## 6. Field Extraction Logic

### 6.1 Dealer Name
- Keyword-based region filtering
- Fuzzy matching against dealer master list
- Consensus across multiple text occurrences

### 6.2 Model Name
- Exact string matching against asset master
- Longest valid match selected

### 6.3 Horse Power
- Regex-based numeric extraction (`XX HP`)
- Cross-validated against known model specifications

### 6.4 Asset Cost
- Context-aware numeric extraction
- Keywords: Total, Amount, Cost, Price
- Sanity bounds applied to filter noise

### 6.5 Dealer Signature & Stamp
- Computer vision-based detection
- Bounding box extraction
- IoU-based validation

---

## 7. Handling Lack of Ground Truth

No labelled dataset is provided.  
The system adopts **real-world strategies** to approximate supervision:

### 7.1 Manual Mini-Sample Annotation
- Small curated subset (20–30 documents)
- Multiple languages and scan qualities
- Used only for validation and calibration

### 7.2 Pseudo-Labeling via Rules
- High-confidence rule outputs treated as pseudo labels
- Thresholds refined iteratively
- No pseudo labels treated as absolute truth

### 7.3 Self-Consistency & Consensus
- Multiple extractors per field
- Agreement increases confidence
- Disagreement triggers fallback logic

This mirrors real-world Document AI deployments where labeled data is limited and reliability is critical.

---

## 8. Confidence Scoring Strategy

Each field receives an independent confidence score based on:
- Extraction method
- Validation checks
- Consensus strength

**Document-level confidence** is computed as:
```

min(field confidences)

```

This aligns with document-level accuracy evaluation and ensures conservative risk estimation.

---

## 9. Output JSON Schema (Guaranteed Contract)

```json
{
  "doc_id": "invoice_001",
  "fields": {
    "dealer_name": "ABC Tractors Pvt Ltd",
    "model_name": "Mahindra 575 DI",
    "horse_power": 50,
    "asset_cost": 525000,
    "signature": {
      "present": true,
      "bbox": [100, 200, 300, 250]
    },
    "stamp": {
      "present": false,
      "bbox": null
    }
  },
  "confidence": 0.96,
  "processing_time_sec": 3.8,
  "cost_estimate_usd": 0.002
}


Schema is **never violated**, even under extraction failure.

---

## 10. Exploratory Data Analysis (EDA)

EDA is performed **offline** to understand:

* Language distribution
* Error patterns
* Field-level failure modes
* Latency behavior

Key insights:

* Handwritten vernacular documents show higher OCR noise
* Asset cost is the most error-prone numeric field
* Vision-based stamp detection is more stable than signature detection

---

## 11. Error Analysis

Common error categories:

* OCR text fragmentation
* Multiple numeric candidates
* Layout ambiguity
* Stamp overlapping with text regions

Error categorization informs rule tuning and confidence calibration.

---

## 12. Cost & Latency Estimation

* Average processing time: ≤ 30 seconds per document
* Inference cost: < $0.01 per document
* Designed for CPU or low-tier GPU deployment

Trade-offs between accuracy and cost are explicitly documented.

---

## 13. How to Run
bash
```
pip install -r requirements.txt
python executable.py --input <pdf_path> --output result.json
```

---

## 14. Repository Structure

```
submission/
├── executable.py
├── requirements.txt
├── README.md
├── utils/
└── sample_output/
    └── result.json
```

---

## 15. Limitations & Future Work

* OCR quality limits downstream accuracy
* Extremely noisy handwritten documents remain challenging
* Future improvements:

  * Active learning
  * Better vision detectors
  * Layout-aware models

---

## 16. Conclusion

This project demonstrates a **production-ready Document AI system** designed for environments with limited ground truth, strict cost constraints, and high reliability requirements.
The emphasis on deterministic logic, validation, and confidence makes it suitable for real-world financial workflows.

---



