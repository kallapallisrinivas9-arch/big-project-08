from __future__ import annotations

import numpy as np
import pandas as pd


REQUIRED_COLUMNS = [
    "station_id",
    "sensor_id",
    "observed_at",
    "temperature_c",
    "relative_humidity_pct",
    "pressure_hpa",
]


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()

    data = df.copy()

    missing = [
        column
        for column in REQUIRED_COLUMNS
        if column not in data.columns
    ]

    if missing:
        raise ValueError(
            f"Missing required columns: {missing}"
        )

    data["observed_at"] = pd.to_datetime(
        data["observed_at"],
        errors="coerce",
        utc=True,
    )

    data = data.sort_values(
        ["station_id", "sensor_id", "observed_at"]
    ).reset_index(drop=True)

    group = data.groupby(
        ["station_id", "sensor_id"],
        sort=False,
    )

    data["temperature_delta"] = group[
        "temperature_c"
    ].diff()

    data["humidity_delta"] = group[
        "relative_humidity_pct"
    ].diff()

    data["pressure_delta"] = group[
        "pressure_hpa"
    ].diff()

    data["temperature_rate"] = (
        data["temperature_delta"]
    )

    data["temperature_rolling_mean"] = group[
        "temperature_c"
    ].transform(
        lambda x: x.rolling(
            window=5,
            min_periods=1,
        ).mean()
    )

    data["temperature_rolling_std"] = group[
        "temperature_c"
    ].transform(
        lambda x: x.rolling(
            window=5,
            min_periods=2,
        ).std()
    ).fillna(0)

    data["humidity_rolling_mean"] = group[
        "relative_humidity_pct"
    ].transform(
        lambda x: x.rolling(
            window=5,
            min_periods=1,
        ).mean()
    )

    data["pressure_rolling_mean"] = group[
        "pressure_hpa"
    ].transform(
        lambda x: x.rolling(
            window=5,
            min_periods=1,
        ).mean()
    )

    data["temperature_deviation"] = (
        data["temperature_c"]
        - data["temperature_rolling_mean"]
    )

    data["pressure_deviation"] = (
        data["pressure_hpa"]
        - data["pressure_rolling_mean"]
    )

    data["temperature_persistence"] = (
        group["temperature_c"]
        .transform(
            lambda x: x.diff().abs()
        )
        .fillna(0)
        .rolling(3, min_periods=1)
        .mean()
    )

    data["humidity_temperature_consistency"] = (
        data["temperature_delta"].fillna(0).abs()
        + data["humidity_delta"].fillna(0).abs() / 10
    )

    data["pressure_consistency"] = (
        data["pressure_delta"]
        .fillna(0)
        .abs()
    )

    data["missing_temperature"] = (
        data["temperature_c"].isna().astype(int)
    )

    data["missing_humidity"] = (
        data["relative_humidity_pct"].isna().astype(int)
    )

    data["missing_pressure"] = (
        data["pressure_hpa"].isna().astype(int)
    )

    data["communication_gap"] = (
        data["temperature_c"].isna()
        & data["relative_humidity_pct"].isna()
        & data["pressure_hpa"].isna()
    ).astype(int)

    data["physics_violation"] = (
        (
            data["relative_humidity_pct"].notna()
            & (
                (data["relative_humidity_pct"] < 0)
                | (data["relative_humidity_pct"] > 100)
            )
        )
        |
        (
            data["pressure_hpa"].notna()
            & (
                (data["pressure_hpa"] < 800)
                | (data["pressure_hpa"] > 1100)
            )
        )
    ).astype(int)

    numeric_features = [
        "temperature_c",
        "relative_humidity_pct",
        "pressure_hpa",
        "temperature_delta",
        "humidity_delta",
        "pressure_delta",
        "temperature_rate",
        "temperature_rolling_mean",
        "temperature_rolling_std",
        "humidity_rolling_mean",
        "pressure_rolling_mean",
        "temperature_deviation",
        "pressure_deviation",
        "temperature_persistence",
        "humidity_temperature_consistency",
        "pressure_consistency",
        "missing_temperature",
        "missing_humidity",
        "missing_pressure",
        "communication_gap",
        "physics_violation",
    ]

    for column in numeric_features:
        data[column] = pd.to_numeric(
            data[column],
            errors="coerce",
        )

    data[numeric_features] = data[
        numeric_features
    ].replace(
        [np.inf, -np.inf],
        np.nan,
    ).fillna(0)

    return data


def get_model_features(
    data: pd.DataFrame,
) -> list[str]:

    candidates = [
        "temperature_c",
        "relative_humidity_pct",
        "pressure_hpa",
        "temperature_delta",
        "humidity_delta",
        "pressure_delta",
        "temperature_deviation",
        "pressure_deviation",
        "temperature_rolling_std",
        "temperature_persistence",
        "humidity_temperature_consistency",
        "pressure_consistency",
        "missing_temperature",
        "missing_humidity",
        "missing_pressure",
        "communication_gap",
        "physics_violation",
    ]

    return [
        column
        for column in candidates
        if column in data.columns
    ]