from __future__ import annotations

import time
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest


@dataclass
class DetectionResult:
    anomaly_score: float
    anomaly_flag: bool
    threshold: float
    model_name: str
    model_version: str
    features_used: list[str]
    inference_time_ms: float


class AnomalyDetector:
    def __init__(
        self,
        contamination: float = 0.08,
        random_state: int = 42,
    ) -> None:

        self.contamination = contamination
        self.random_state = random_state
        self.model: IsolationForest | None = None
        self.threshold = 0.0

    def fit(
        self,
        data: pd.DataFrame,
        features: list[str],
    ) -> None:

        if data.empty or not features:
            self.model = None
            return

        x = (
            data[features]
            .replace([np.inf, -np.inf], np.nan)
            .fillna(0)
        )

        if len(x) < 10:
            self.model = None
            return

        self.model = IsolationForest(
            n_estimators=200,
            contamination=self.contamination,
            random_state=self.random_state,
        )

        self.model.fit(x)

        scores = -self.model.score_samples(x)

        self.threshold = float(
            np.quantile(
                scores,
                1 - self.contamination,
            )
        )

    def predict(
        self,
        row: pd.Series,
        features: list[str],
    ) -> DetectionResult:

        start = time.perf_counter()

        if self.model is None:
            return DetectionResult(
                anomaly_score=0.0,
                anomaly_flag=False,
                threshold=0.0,
                model_name="IsolationForest",
                model_version="1.0",
                features_used=features,
                inference_time_ms=(
                    time.perf_counter() - start
                ) * 1000,
            )

        values = (
            pd.DataFrame([row[features]])
            .replace([np.inf, -np.inf], np.nan)
            .fillna(0)
        )

        score = float(
            -self.model.score_samples(values)[0]
        )

        flag = score >= self.threshold

        elapsed = (
            time.perf_counter() - start
        ) * 1000

        return DetectionResult(
            anomaly_score=score,
            anomaly_flag=bool(flag),
            threshold=float(self.threshold),
            model_name="IsolationForest",
            model_version="1.0",
            features_used=features,
            inference_time_ms=float(elapsed),
        )