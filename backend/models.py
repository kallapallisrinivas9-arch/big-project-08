from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    Integer,
    JSON,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column

from backend.database import Base


class Observation(Base):
    __tablename__ = "observations"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    observation_id: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
    )

    station_id: Mapped[str] = mapped_column(
        String(100),
        index=True,
    )

    sensor_id: Mapped[str] = mapped_column(
        String(100),
        index=True,
    )

    observed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        index=True,
    )

    received_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    temperature_c: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    relative_humidity_pct: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    pressure_hpa: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    source: Mapped[str] = mapped_column(
        String(50)
    )

    sequence_number: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )


class AnomalyResult(Base):
    __tablename__ = "anomaly_results"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    observation_id: Mapped[str] = mapped_column(
        String(100),
        index=True,
    )

    station_id: Mapped[str] = mapped_column(
        String(100)
    )

    sensor_id: Mapped[str] = mapped_column(
        String(100)
    )

    anomaly_score: Mapped[float] = mapped_column(
        Float
    )

    anomaly_flag: Mapped[bool] = mapped_column(
        Boolean
    )

    threshold: Mapped[float] = mapped_column(
        Float
    )

    model_name: Mapped[str] = mapped_column(
        String(100)
    )

    model_version: Mapped[str] = mapped_column(
        String(50)
    )

    state: Mapped[str] = mapped_column(
        String(50)
    )

    root_cause: Mapped[str] = mapped_column(
        String(100)
    )

    confidence: Mapped[str] = mapped_column(
        String(30)
    )

    explanation: Mapped[str] = mapped_column(
        Text
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True)
    )


class Evidence(Base):
    __tablename__ = "evidence"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    observation_id: Mapped[str] = mapped_column(
        String(100),
        index=True,
    )

    evidence_json: Mapped[dict] = mapped_column(
        JSON
    )


class Correction(Base):
    __tablename__ = "corrections"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    observation_id: Mapped[str] = mapped_column(
        String(100),
        index=True,
    )

    original_value: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    corrected_value: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    method: Mapped[str] = mapped_column(
        String(100)
    )

    decision: Mapped[str] = mapped_column(
        String(50)
    )

    confidence: Mapped[str] = mapped_column(
        String(30)
    )

    reason: Mapped[str] = mapped_column(
        Text
    )

    model_version: Mapped[str] = mapped_column(
        String(50)
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True)
    )


class SensorHealth(Base):
    __tablename__ = "sensor_health"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    station_id: Mapped[str] = mapped_column(
        String(100),
        index=True,
    )

    sensor_id: Mapped[str] = mapped_column(
        String(100),
        index=True,
    )

    health_score: Mapped[float] = mapped_column(
        Float
    )

    status: Mapped[str] = mapped_column(
        String(30)
    )

    trend: Mapped[str] = mapped_column(
        String(30)
    )

    maintenance_risk: Mapped[str] = mapped_column(
        String(30)
    )

    anomaly_frequency: Mapped[float] = mapped_column(
        Float
    )

    communication_reliability: Mapped[float] = mapped_column(
        Float
    )


class Alert(Base):
    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    alert_type: Mapped[str] = mapped_column(
        String(50)
    )

    severity: Mapped[str] = mapped_column(
        String(30)
    )

    station_id: Mapped[str] = mapped_column(
        String(100)
    )

    sensor_id: Mapped[str] = mapped_column(
        String(100)
    )

    message: Mapped[str] = mapped_column(
        Text
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True)
    )

    status: Mapped[str] = mapped_column(
        String(30)
    )


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    entity_type: Mapped[str] = mapped_column(
        String(100)
    )

    entity_id: Mapped[str] = mapped_column(
        String(100)
    )

    action: Mapped[str] = mapped_column(
        String(100)
    )

    previous_state: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )

    new_state: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )

    actor: Mapped[str] = mapped_column(
        String(100)
    )

    reason: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True)
    )