import pandas as pd

from backend.ml.feature_engineering import (
    build_features,
    get_model_features,
)
from backend.simulation.data_generator import (
    generate_weather_data,
)


def test_feature_generation():

    data = generate_weather_data(
        stations=1,
        records_per_station=20,
        seed=42,
    )

    features = build_features(data)

    assert not features.empty

    assert "temperature_delta" in features.columns
    assert "temperature_rolling_mean" in features.columns
    assert "physics_violation" in features.columns


def test_model_features():

    data = generate_weather_data(
        stations=1,
        records_per_station=20,
        seed=42,
    )

    features = build_features(data)

    model_features = get_model_features(
        features
    )

    assert len(model_features) > 5