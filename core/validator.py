from typing import List, Dict, Optional


class ConfidenceScorer:
    """
    Computes field-level and document-level confidence scores.
    All confidence values are normalized between 0.0 and 1.0.
    """

    # -------- Text Fields -------- #

    def dealer_name_confidence(
        self,
        fuzzy_score: float,
        region: Optional[str] = None
    ) -> float:
        """
        Confidence based on fuzzy match score and layout region.
        """
        score = fuzzy_score

        if region == "header":
            score += 0.05

        return round(min(score, 1.0), 2)

    def exact_text_confidence(self, matched: bool) -> float:
        """
        For exact matches like Model Name.
        """
        return 1.0 if matched else 0.0

    # -------- Numeric Fields -------- #

    def numeric_confidence(
        self,
        exact_match: bool,
        sanity_check_passed: bool = True
    ) -> float:
        """
        Numeric confidence (Horse Power, Asset Cost).
        """
        if exact_match and sanity_check_passed:
            return 1.0
        if exact_match:
            return 0.85
        return 0.6

    # -------- Presence Fields -------- #

    def presence_confidence(
        self,
        present: bool,
        iou: Optional[float] = None
    ) -> float:
        """
        Confidence for signature/stamp detection.
        """
        # If absent, and we are sure it's absent
        if not present:
            return 1.0

        # Present but IoU known
        if iou is not None:
            return round(min(0.5 + iou / 2, 1.0), 2)

        # Present but no IoU (fallback)
        return 0.7

    # -------- Aggregation -------- #

    def document_confidence(self, field_confidences: List[float]) -> float:
        """
        Conservative aggregation strategy:
        document confidence = minimum field confidence
        """
        if not field_confidences:
            return 0.0

        return round(min(field_confidences), 2)
