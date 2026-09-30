from backend.ml.anomaly_detector import (
    AnomalyDetector,
)
from backend.ml.correction_engine import (
    decide_correction,
)
from backend.ml.evidence_fusion import (
    fuse_evidence,
)
from backend.ml.feature_engineering import (
    build_features,
    get_model_features,
)
from backend.services.pipeline import run_pipeline
from backend.simulation.data_generator import (
    generate_weather_data,
)
from backend.simulation.fault_injection import (
    inject_faults,
)


def test_anomaly_detector():

    data = generate_weather_data(
        stations=2,
        records_per_station=30,
        seed=42,
    )

    features = build_features(data)

    model_features = get_model_features(
        features
    )

    detector = AnomalyDetector(
        random_state=42
    )

    detector.fit(
        features,
        model_features,
    )

    result = detector.predict(
        features.iloc[0],
        model_features,
    )

    assert isinstance(
        result.anomaly_score,
        float,
    )

    assert isinstance(
        result.anomaly_flag,
        bool,
    )


def test_evidence_fusion():

    row = {
        "temperature_deviation": 10,
        "temperature_rolling_std": 7,
        "temperature_delta": 10,
        "humidity_delta": 25,
        "communication_gap": 0,
        "physics_violation": 0,
    }

    result = fuse_evidence(
        row,
        anomaly_score=0.9,
        anomaly_flag=True,
    )

    assert result["state"] in {
        "NORMAL",
        "SENSOR_FAULT",
        "GENUINE_WEATHER_EVENT",
        "COMMUNICATION_FAULT",
        "UNCERTAIN",
    }


def test_genuine_weather_event_detection():

    row = {
        "temperature_deviation": 6.5,
        "temperature_rolling_std": 2.0,
        "temperature_delta": 5.5,
        "humidity_delta": 12.0,
        "communication_gap": 0,
        "physics_violation": 0,
    }

    result = fuse_evidence(
        row,
        anomaly_score=0.8,
        anomaly_flag=True,
    )

    assert result["state"] == "GENUINE_WEATHER_EVENT"
    assert result["root_cause"] == "GENUINE_WEATHER_EVENT"


def test_correction_engine():

    row = {
        "temperature_c": 40.0,
        "temperature_rolling_mean": 25.0,
    }

    decision = {
        "state": "SENSOR_FAULT",
        "confidence": "HIGH",
        "explanation": "Sensor spike detected.",
    }

    result = decide_correction(
        row,
        decision,
    )

    assert result["decision"] == "AUTO_CORRECT"
    assert result["original_value"] == 40.0
    assert result["corrected_value"] == 25.0


def test_complete_pipeline():

    data = generate_weather_data(
        stations=3,
        records_per_station=50,
        seed=42,
    )

    injected, _ = inject_faults(
        data,
        seed=42,
    )

    result = run_pipeline(
        injected,
        seed=42,
    )

    assert "observations" in result
    assert "anomalies" in result
    assert "alerts" in result
    assert "sensor_health" in result

    assert len(result["observations"]) > 0
    assert len(result["sensor_health"]) > 0