from __future__ import annotations

from typing import Any

import pandas as pd

from backend.ml.anomaly_detector import AnomalyDetector
from backend.ml.correction_engine import decide_correction
from backend.ml.evidence_fusion import fuse_evidence
from backend.ml.feature_engineering import (
    build_features,
    get_model_features,
)
from backend.ml.health_engine import calculate_sensor_health
from backend.services.alert_service import create_alert


def run_pipeline(
    data: pd.DataFrame,
    seed: int = 42,
) -> dict[str, Any]:

    if data.empty:
        return {
            "observations": [],
            "anomalies": [],
            "alerts": [],
            "sensor_health": [],
        }

    features = build_features(data)

    model_features = get_model_features(features)

    detector = AnomalyDetector(
        random_state=seed
    )

    detector.fit(
        features,
        model_features,
    )

    anomalies = []
    enriched_rows = []

    for _, row in features.iterrows():

        detection = detector.predict(
            row,
            model_features,
        )

        decision = fuse_evidence(
            row.to_dict(),
            detection.anomaly_score,
            detection.anomaly_flag,
        )

        correction = decide_correction(
            row.to_dict(),
            decision,
        )

        result = {
            "observation_id": row.get(
                "observation_id"
            ),
            "station_id": row.get(
                "station_id"
            ),
            "sensor_id": row.get(
                "sensor_id"
            ),
            "observed_at": row.get(
                "observed_at"
            ),
            "temperature_c": row.get(
                "temperature_c"
            ),
            "relative_humidity_pct": row.get(
                "relative_humidity_pct"
            ),
            "pressure_hpa": row.get(
                "pressure_hpa"
            ),
            "anomaly_score": detection.anomaly_score,
            "anomaly_flag": detection.anomaly_flag,
            "threshold": detection.threshold,
            "model_name": detection.model_name,
            "model_version": detection.model_version,
            "features_used": detection.features_used,
            "inference_time_ms": detection.inference_time_ms,
            "state": decision["state"],
            "root_cause": decision["root_cause"],
            "confidence": decision["confidence"],
            "confidence_score": decision[
                "confidence_score"
            ],
            "evidence": decision["evidence"],
            "explanation": decision["explanation"],
            "correction": correction,
        }

        anomalies.append(result)

        enriched_rows.append(
            {
                **row.to_dict(),
                "anomaly_flag": detection.anomaly_flag,
                "communication_fault": (
                    decision["state"]
                    == "COMMUNICATION_FAULT"
                ),
            }
        )

    enriched_df = pd.DataFrame(enriched_rows)

    health = calculate_sensor_health(
        enriched_df
    )

    alerts = []

    for anomaly in anomalies:

        alert = create_alert(anomaly)

        if alert is not None:
            alerts.append(alert)

    return {
        "observations": features.to_dict(
            orient="records"
        ),
        "anomalies": anomalies,
        "alerts": alerts,
        "sensor_health": health.to_dict(
            orient="records"
        ),
    }