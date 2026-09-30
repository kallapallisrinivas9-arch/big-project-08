from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ObservationInput(BaseModel):
    observation_id: str
    station_id: str
    sensor_id: str
    observed_at: datetime
    received_at: datetime | None = None

    temperature_c: float | None = None
    relative_humidity_pct: float | None = None
    pressure_hpa: float | None = None

    source: str = "api"
    sequence_number: int | None = None

    model_config = ConfigDict(
        extra="allow"
    )


class AnalyzeRequest(BaseModel):
    observations: list[ObservationInput] = Field(
        min_length=1,
        max_length=10000,
    )


class SimulateRequest(BaseModel):
    stations: int = Field(default=4, ge=1, le=50)
    records_per_station: int = Field(
        default=120,
        ge=10,
        le=5000,
    )
    seed: int = 42
    inject_faults: bool = True


class CorrectionRequest(BaseModel):
    observation_id: str
    temperature_c: float | None = None


class APIResponse(BaseModel):
    success: bool
    data: Any = None
    error: str | None = None
    meta: dict[str, Any] | None = None