from __future__ import annotations

from typing import Any


STATES = [
    "NORMAL",
    "SENSOR_FAULT",
    "GENUINE_WEATHER_EVENT",
    "COMMUNICATION_FAULT",
    "UNCERTAIN",
]

ROOT_CAUSES = [
    "SPIKE",
    "FROZEN_SENSOR",
    "DRIFT",
    "NOISE",
    "COMMUNICATION_FAILURE",
    "DATA_CORRUPTION",
    "MULTIVARIATE_INCONSISTENCY",
    "GENUINE_WEATHER_EVENT",
    "UNKNOWN",
]


def _confidence(score: float) -> str:
    if score >= 0.90:
        return "VERY_HIGH"
    if score >= 0.75:
        return "HIGH"
    if score >= 0.50:
        return "MEDIUM"
    return "LOW"


def fuse_evidence(
    row: dict[str, Any],
    anomaly_score: float,
    anomaly_flag: bool,
) -> dict[str, Any]:

    evidence = {
        "physics": 0.0,
        "temporal": 0.0,
        "statistical": 0.0,
        "ml": 0.0,
        "multivariate": 0.0,
        "spatial": None,
        "communication": 0.0,
        "data_quality": 0.0,
    }

    if anomaly_flag:
        evidence["ml"] = min(1.0, anomaly_score)

    if row.get("physics_violation", 0):
        evidence["physics"] = 1.0
        evidence["data_quality"] = 0.9

    if abs(row.get("temperature_deviation", 0)) > 5:
        evidence["temporal"] = 0.85

    if row.get("temperature_rolling_std", 0) > 4:
        evidence["statistical"] = 0.85

    if row.get("communication_gap", 0):
        evidence["communication"] = 1.0

    if (
        abs(row.get("temperature_delta", 0)) > 8
        and abs(row.get("humidity_delta", 0)) > 20
    ):
        evidence["multivariate"] = 0.9

    reasons = []

    if evidence["communication"] >= 0.8:
        state = "COMMUNICATION_FAULT"
        root_cause = "COMMUNICATION_FAILURE"
        reasons.append(
            "Multiple weather values are missing."
        )

    elif evidence["physics"] >= 0.8:
        state = "SENSOR_FAULT"
        root_cause = "DATA_CORRUPTION"
        reasons.append(
            "Physical range validation failed."
        )

    elif evidence["multivariate"] >= 0.8:
        state = "SENSOR_FAULT"
        root_cause = "MULTIVARIATE_INCONSISTENCY"
        reasons.append(
            "Temperature and humidity changed inconsistently."
        )

    elif (
        anomaly_flag
        and abs(row.get("temperature_deviation", 0)) > 4
        and abs(row.get("temperature_delta", 0)) <= 12
        and abs(row.get("humidity_delta", 0)) >= 8
        and row.get("temperature_rolling_std", 0) <= 4
        and not row.get("communication_gap", 0)
        and not row.get("physics_violation", 0)
    ):
        state = "GENUINE_WEATHER_EVENT"
        root_cause = "GENUINE_WEATHER_EVENT"
        reasons.append(
            "A coordinated temperature and humidity shift without sensor or communication faults matches a genuine weather event."
        )

    elif anomaly_flag and evidence["temporal"] >= 0.8:
        state = "SENSOR_FAULT"
        root_cause = "SPIKE"
        reasons.append(
            "Abrupt deviation detected against recent history."
        )

    elif anomaly_flag:
        state = "UNCERTAIN"
        root_cause = "UNKNOWN"
        reasons.append(
            "ML model detected an anomaly but evidence "
            "is insufficient for a definitive root cause."
        )

    else:
        state = "NORMAL"
        root_cause = "UNKNOWN"
        reasons.append(
            "No strong anomaly evidence was detected."
        )

    active_scores = [
        value
        for value in evidence.values()
        if value is not None
    ]

    confidence_score = (
        max(active_scores)
        if active_scores
        else 0.0
    )

    if state == "NORMAL":
        confidence_score = max(
            0.70,
            1.0 - anomaly_score,
        )

    return {
        "state": state,
        "root_cause": root_cause,
        "confidence": _confidence(
            float(confidence_score)
        ),
        "confidence_score": float(
            min(1.0, confidence_score)
        ),
        "evidence": evidence,
        "explanation": " ".join(reasons),
    }