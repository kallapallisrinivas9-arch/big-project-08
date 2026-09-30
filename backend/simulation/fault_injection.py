from __future__ import annotations

from typing import Optional

import numpy as np
import pandas as pd


FAULT_TYPES = [
    "SPIKE",
    "FROZEN_SENSOR",
    "DRIFT",
    "NOISE",
    "COMMUNICATION_FAILURE",
    "DATA_CORRUPTION",
    "MULTIVARIATE_INCONSISTENCY",
]


def inject_faults(
    df: pd.DataFrame,
    seed: int = 42,
    fault_types: Optional[list[str]] = None,
) -> tuple[pd.DataFrame, pd.DataFrame]:

    if df.empty:
        return df.copy(), pd.DataFrame()

    rng = np.random.default_rng(seed)

    result = df.copy()
    result["source_observation_id"] = result["observation_id"]
    result["is_injected"] = False
    result["fault_type"] = None
    result["scenario_id"] = None
    result["injection_version"] = "1.0"

    ground_truth = []

    selected_faults = fault_types or FAULT_TYPES

    for fault_index, fault_type in enumerate(selected_faults):

        if fault_type not in FAULT_TYPES:
            continue

        station_ids = result["station_id"].dropna().unique()

        if len(station_ids) == 0:
            continue

        station_id = station_ids[
            fault_index % len(station_ids)
        ]

        candidate_indices = result.index[
            result["station_id"] == station_id
        ].tolist()

        if len(candidate_indices) < 10:
            continue

        start_position = int(
            rng.integers(
                2,
                max(3, len(candidate_indices) - 5),
            )
        )

        duration = min(
            5,
            len(candidate_indices) - start_position,
        )

        selected_indices = candidate_indices[
            start_position:start_position + duration
        ]

        scenario_id = f"SCN-{fault_index + 1:03d}"

        original_values = result.loc[
            selected_indices,
            [
                "temperature_c",
                "relative_humidity_pct",
                "pressure_hpa",
            ],
        ].copy()

        if fault_type == "SPIKE":
            result.loc[selected_indices, "temperature_c"] += (
                15.0
            )

        elif fault_type == "FROZEN_SENSOR":
            frozen_value = result.loc[
                selected_indices[0],
                "temperature_c",
            ]

            result.loc[
                selected_indices,
                "temperature_c",
            ] = frozen_value

        elif fault_type == "DRIFT":
            drift_values = np.linspace(
                0.5,
                8.0,
                len(selected_indices),
            )

            result.loc[
                selected_indices,
                "temperature_c",
            ] += drift_values

        elif fault_type == "NOISE":
            noise = rng.normal(
                0,
                6,
                len(selected_indices),
            )

            result.loc[
                selected_indices,
                "temperature_c",
            ] += noise

        elif fault_type == "COMMUNICATION_FAILURE":
            result.loc[
                selected_indices,
                [
                    "temperature_c",
                    "relative_humidity_pct",
                    "pressure_hpa",
                ],
            ] = np.nan

        elif fault_type == "DATA_CORRUPTION":
            result.loc[
                selected_indices,
                "relative_humidity_pct",
            ] = 150.0

        elif fault_type == "MULTIVARIATE_INCONSISTENCY":
            result.loc[
                selected_indices,
                "temperature_c",
            ] += 12.0

            result.loc[
                selected_indices,
                "relative_humidity_pct",
            ] = np.clip(
                result.loc[
                    selected_indices,
                    "relative_humidity_pct",
                ] - 35,
                0,
                100,
            )

        result.loc[
            selected_indices,
            "is_injected",
        ] = True

        result.loc[
            selected_indices,
            "fault_type",
        ] = fault_type

        result.loc[
            selected_indices,
            "scenario_id",
        ] = scenario_id

        for position, row_index in enumerate(selected_indices):

            original = original_values.loc[row_index]
            modified = result.loc[row_index]

            ground_truth.append(
                {
                    "observation_id": modified[
                        "observation_id"
                    ],
                    "station_id": modified["station_id"],
                    "sensor_id": modified["sensor_id"],
                    "observed_at": modified["observed_at"],
                    "is_injected": True,
                    "fault_type": fault_type,
                    "original_temperature_c": original[
                        "temperature_c"
                    ],
                    "injected_temperature_c": modified[
                        "temperature_c"
                    ],
                    "original_relative_humidity_pct": original[
                        "relative_humidity_pct"
                    ],
                    "injected_relative_humidity_pct": modified[
                        "relative_humidity_pct"
                    ],
                    "original_pressure_hpa": original[
                        "pressure_hpa"
                    ],
                    "injected_pressure_hpa": modified[
                        "pressure_hpa"
                    ],
                    "fault_start": result.loc[
                        selected_indices[0],
                        "observed_at",
                    ],
                    "fault_end": result.loc[
                        selected_indices[-1],
                        "observed_at",
                    ],
                    "severity": "HIGH",
                    "injection_parameters": {
                        "position": position,
                        "seed": seed,
                    },
                    "random_seed": seed,
                    "source_observation_id": modified[
                        "source_observation_id"
                    ],
                    "scenario_id": scenario_id,
                    "injection_version": "1.0",
                }
            )

    return result, pd.DataFrame(ground_truth)