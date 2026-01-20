OUTPUT_SCHEMA = {
    "doc_id": "",

    "fields": {
        "dealer_name": "",
        "model_name": "",
        "horse_power": 0,          # numeric default
        "asset_cost": 0,           # numeric default

        "signature": {
            "present": False,
            "bbox": []              # empty list, not None
        },

        "stamp": {
            "present": False,
            "bbox": []
        }
    },

    # optional but VERY useful internally
    "field_confidence": {
        "dealer_name": 0.0,
        "model_name": 0.0,
        "horse_power": 0.0,
        "asset_cost": 0.0,
        "signature": 0.0,
        "stamp": 0.0
    },

    "confidence": 0.0,
    "processing_time_sec": 0.0,
    "cost_estimate_usd": 0.0
}
