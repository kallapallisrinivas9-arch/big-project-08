from __future__ import annotations

from datetime import datetime, timezone

import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.database import init_db
from backend.schemas import (
    AnalyzeRequest,
    APIResponse,
    CorrectionRequest,
    SimulateRequest,
)
from backend.services.pipeline import run_pipeline
from backend.simulation.data_generator import (
    generate_weather_data,
)
from backend.simulation.fault_injection import (
    inject_faults,
)


app = FastAPI(
    title="WeatherGuard AI",
    description=(
        "AI/ML based intelligent anomaly detection "
        "for Automatic Weather Stations."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


LATEST_RESULT = {
    "observations": [],
    "anomalies": [],
    "alerts": [],
    "sensor_health": [],
}


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get(
    "/health",
    response_model=APIResponse,
)
def health():
    return APIResponse(
        success=True,
        data={
            "service": "WeatherGuard AI",
            "status": "running",
            "timestamp": datetime.now(
                timezone.utc
            ),
        },
    )


@app.get(
    "/stations",
    response_model=APIResponse,
)
def stations():

    ids = sorted(
        {
            item["station_id"]
            for item in LATEST_RESULT["observations"]
            if item.get("station_id")
        }
    )

    return APIResponse(
        success=True,
        data=ids,
    )


@app.get(
    "/sensors",
    response_model=APIResponse,
)
def sensors():

    sensors_data = sorted(
        {
            (
                item["station_id"],
                item["sensor_id"],
            )
            for item in LATEST_RESULT["observations"]
            if item.get("sensor_id")
        }
    )

    return APIResponse(
        success=True,
        data=[
            {
                "station_id": station,
                "sensor_id": sensor,
            }
            for station, sensor in sensors_data
        ],
    )


@app.get(
    "/observations",
    response_model=APIResponse,
)
def observations():

    return APIResponse(
        success=True,
        data=LATEST_RESULT["observations"][
            -100:
        ],
    )


@app.get(
    "/anomalies",
    response_model=APIResponse,
)
def anomalies():

    return APIResponse(
        success=True,
        data=[
            item
            for item in LATEST_RESULT["anomalies"]
            if item["anomaly_flag"]
        ][-100:],
    )


@app.get(
    "/alerts",
    response_model=APIResponse,
)
def alerts():

    return APIResponse(
        success=True,
        data=LATEST_RESULT["alerts"][-100:],
    )


@app.get(
    "/sensor-health",
    response_model=APIResponse,
)
def sensor_health():

    return APIResponse(
        success=True,
        data=LATEST_RESULT["sensor_health"],
    )


@app.post(
    "/simulate",
    response_model=APIResponse,
)
def simulate(request: SimulateRequest):

    global LATEST_RESULT

    data = generate_weather_data(
        stations=request.stations,
        records_per_station=request.records_per_station,
        seed=request.seed,
    )

    if request.inject_faults:
        data, ground_truth = inject_faults(
            data,
            seed=request.seed,
        )
    else:
        ground_truth = pd.DataFrame()

    result = run_pipeline(
        data,
        seed=request.seed,
    )

    result["ground_truth"] = (
        ground_truth.to_dict(
            orient="records"
        )
        if not ground_truth.empty
        else []
    )

    LATEST_RESULT = result

    return APIResponse(
        success=True,
        data=result,
        meta={
            "synthetic_demo": True,
            "seed": request.seed,
        },
    )


@app.post(
    "/analyze",
    response_model=APIResponse,
)
def analyze(request: AnalyzeRequest):

    global LATEST_RESULT

    if not request.observations:
        raise HTTPException(
            status_code=400,
            detail="No observations supplied.",
        )

    data = pd.DataFrame(
        [
            observation.model_dump()
            for observation in request.observations
        ]
    )

    result = run_pipeline(data)

    LATEST_RESULT = result

    return APIResponse(
        success=True,
        data=result,
        meta={
            "synthetic_demo": False,
        },
    )


@app.post(
    "/correct",
    response_model=APIResponse,
)
def correct(request: CorrectionRequest):

    for anomaly in LATEST_RESULT["anomalies"]:

        if (
            anomaly.get("observation_id")
            == request.observation_id
        ):

            correction = anomaly["correction"]

            if request.temperature_c is not None:
                correction[
                    "corrected_value"
                ] = request.temperature_c

            correction["decision"] = (
                "HUMAN_REVIEW"
            )

            return APIResponse(
                success=True,
                data=correction,
            )

    raise HTTPException(
        status_code=404,
        detail="Observation not found.",
    )