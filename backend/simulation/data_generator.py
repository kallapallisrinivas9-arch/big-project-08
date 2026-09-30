from __future__ import annotations

from datetime import datetime, timedelta, timezone

import numpy as np
import pandas as pd


def generate_weather_data(
    stations: int = 4,
    records_per_station: int = 120,
    seed: int = 42,
) -> pd.DataFrame:
    """Generate synthetic AWS observations for demo/testing."""

    if stations <= 0 or records_per_station <= 0:
        return pd.DataFrame()

    rng = np.random.default_rng(seed)

    start_time = (
        datetime.now(timezone.utc)
        .replace(minute=0, second=0, microsecond=0)
        - timedelta(hours=records_per_station)
    )

    rows = []

    for station_index in range(stations):
        station_id = f"STN-{station_index + 1:04d}"
        sensor_id = f"SNS-{station_index + 1:04d}"

        base_temperature = 24 + rng.normal(0, 1)
        base_humidity = 65 + rng.normal(0, 3)
        base_pressure = 1013 + rng.normal(0, 2)

        phase = rng.uniform(0, 2 * np.pi)

        for i in range(records_per_station):
            observed_at = start_time + timedelta(hours=i)

            daily_variation = 3.5 * np.sin(
                (2 * np.pi * i / 24) + phase
            )

            temperature = (
                base_temperature
                + daily_variation
                + rng.normal(0, 0.45)
            )

            humidity = (
                base_humidity
                - daily_variation * 2
                + rng.normal(0, 2)
            )

            humidity = float(np.clip(humidity, 15, 98))

            pressure = base_pressure + rng.normal(0, 0.8)

            rows.append(
                {
                    "observation_id": (
                        f"OBS-{station_index + 1:04d}-{i:05d}"
                    ),
                    "station_id": station_id,
                    "sensor_id": sensor_id,
                    "observed_at": observed_at,
                    "received_at": observed_at
                    + timedelta(
                        seconds=int(rng.integers(1, 15))
                    ),
                    "temperature_c": round(float(temperature), 3),
                    "relative_humidity_pct": round(humidity, 3),
                    "pressure_hpa": round(float(pressure), 3),
                    "source": "simulator",
                    "sequence_number": i + 1,
                }
            )

    return pd.DataFrame(rows)


if __name__ == "__main__":
    data = generate_weather_data()

    print(f"Generated {len(data)} observations.")

    data.to_csv(
        "data/processed/synthetic_weather.csv",
        index=False,
    )

    print("Saved to data/processed/synthetic_weather.csv")