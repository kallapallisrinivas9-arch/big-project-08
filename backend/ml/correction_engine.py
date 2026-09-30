from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


def decide_correction(
    row: dict[str, Any],
    decision: dict[str, Any],
) -> dict[str, Any]:

    state = decision["state"]
    confidence = decision["confidence"]

    original = row.get("temperature_c")

    corrected = original
    method = "NONE"

    if (
        state == "SENSOR_FAULT"
        and confidence in {"HIGH", "VERY_HIGH"}
        and original is not None
    ):
        rolling_mean = row.get(
            "temperature_rolling_mean"
        )

        if rolling_mean is not None:
            corrected = float(rolling_mean)
            method = "ROLLING_MEDIAN_PROXY"

            correction_decision = "AUTO_CORRECT"

        else:
            correction_decision = "HUMAN_REVIEW"

    elif state == "SENSOR_FAULT":
        correction_decision = "HUMAN_REVIEW"

    elif state == "COMMUNICATION_FAULT":
        correction_decision = "DO_NOT_CORRECT"

    elif state == "GENUINE_WEATHER_EVENT":
        correction_decision = "DO_NOT_CORRECT"

    elif state == "UNCERTAIN":
        correction_decision = "HUMAN_REVIEW"

    else:
        correction_decision = "DO_NOT_CORRECT"

    return {
        "decision": correction_decision,
        "original_value": original,
        "corrected_value": corrected,
        "method": method,
        "confidence": confidence,
        "reason": decision["explanation"],
        "model_version": "1.0",
        "timestamp": datetime.now(
            timezone.utc
        ),
    }