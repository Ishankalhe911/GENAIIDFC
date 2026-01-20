from typing import Dict, Any
from output.schema import OUTPUT_SCHEMA


class  OutputValidator:
    """
    Ensures output JSON strictly follows schema.py.
    Never allows missing keys or datatype drift.
    """

    def __init__(self):
        self.schema = OUTPUT_SCHEMA

    def _validate_field(self, key: str, value: Any, default: Any):
        """
        If value is None or invalid, fallback to schema default.
        """
        if value is None:
            return default

        expected_type = type(default)

        # Special case for nested dicts (signature, stamp)
        if isinstance(default, dict):
            if not isinstance(value, dict):
                return default

            validated = {}
            for sub_key, sub_default in default.items():
                validated[sub_key] = value.get(sub_key, sub_default)
            return validated

        # Type mismatch
        if not isinstance(value, expected_type):
            return default

        return value

    def validate(self, raw_output: Dict) -> Dict:
        """
        Validate and sanitize final output.
        """
        validated = {}

        for key, default_val in self.schema.items():
            validated[key] = self._validate_field(
                key,
                raw_output.get(key),
                default_val
            )

        return validated
