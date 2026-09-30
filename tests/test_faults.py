from backend.simulation.data_generator import (
    generate_weather_data,
)
from backend.simulation.fault_injection import (
    FAULT_TYPES,
    inject_faults,
)


def test_all_fault_types_supported():

    assert len(FAULT_TYPES) == 7

    expected = {
        "SPIKE",
        "FROZEN_SENSOR",
        "DRIFT",
        "NOISE",
        "COMMUNICATION_FAILURE",
        "DATA_CORRUPTION",
        "MULTIVARIATE_INCONSISTENCY",
    }

    assert set(FAULT_TYPES) == expected


def test_fault_injection_reproducible():

    data = generate_weather_data(
        stations=3,
        records_per_station=40,
        seed=42,
    )

    injected_a, truth_a = inject_faults(
        data,
        seed=100,
    )

    injected_b, truth_b = inject_faults(
        data,
        seed=100,
    )

    assert injected_a.equals(injected_b)
    assert truth_a.equals(truth_b)


def test_fault_lineage():

    data = generate_weather_data(
        stations=3,
        records_per_station=40,
        seed=42,
    )

    injected, truth = inject_faults(
        data,
        seed=42,
    )

    assert "source_observation_id" in injected.columns
    assert "is_injected" in injected.columns

    if not truth.empty:
        assert (
            "source_observation_id"
            in truth.columns
        )