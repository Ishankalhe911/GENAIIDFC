# output/schema.py

from typing import Dict, Any, Optional
import time


def _empty_field(value=None, confidence: float = 0.0) -> Dict[str, Any]:
    """
    Standard field container.
    """
    return {
        "value": value,
        "confidence": round(float(confidence), 3)
    }


def _empty_visual_field() -> Dict[str, Any]:
    """
    For signature / stamp fields.
    """
    return {
        "present": False,
        "bbox": None,
        "confidence": 0.0
    }


def build_empty_output(doc_id: str) -> Dict[str, Any]:
    """
    Builds a guaranteed-valid output skeleton.
    This MUST NEVER fail.
    """

    return {
        "doc_id": doc_id,

        "dealer_name": _empty_field(),
        "model_name": _empty_field(),
        "horse_power": _empty_field(),
        "asset_cost": _empty_field(),

        "dealer_signature": _empty_visual_field(),
        "dealer_stamp": _empty_visual_field(),

        "document_confidence": 0.0,
        "processing_time_sec": 0.0
    }


def update_text_field(
    output: Dict[str, Any],
    field_name: str,
    value: Optional[Any],
    confidence: float
) -> None:
    """
    Updates a text / numeric field safely.
    """

    if field_name not in output:
        # Schema safety: ignore unknown fields silently
        return

    output[field_name]["value"] = value
    output[field_name]["confidence"] = round(float(confidence), 3)


def update_visual_field(
    output: Dict[str, Any],
    field_name: str,
    present: bool,
    bbox: Optional[list],
    confidence: float
) -> None:
    """
    Updates signature / stamp fields.
    """

    if field_name not in output:
        return

    output[field_name]["present"] = bool(present)
    output[field_name]["bbox"] = bbox if present else None
    output[field_name]["confidence"] = round(float(confidence), 3)


def finalize_output(
    output: Dict[str, Any],
    start_time: float
) -> Dict[str, Any]:
    """
    Computes document-level confidence and processing time.
    """

    field_confidences = []

    for key in [
        "dealer_name",
        "model_name",
        "horse_power",
        "asset_cost",
        "dealer_signature",
        "dealer_stamp"
    ]:
        field = output.get(key, {})
        conf = field.get("confidence", 0.0)
        field_confidences.append(conf)

    # Conservative document confidence
    output["document_confidence"] = round(
        min(field_confidences) if field_confidences else 0.0,
        3
    )

    output["processing_time_sec"] = round(
        time.time() - start_time,
        2
    )

    return output
