import React from "react";

export default function SensorCard({
  sensor,
}) {
  const health =
    Number(sensor.health_score ?? 0);

  const status =
    sensor.status ?? "UNKNOWN";

  return (
    <div
      style={{
        background: "#102219",
        border: "1px solid #274634",
        borderRadius: 14,
        padding: 18,
        minWidth: 250,
      }}
    >
      <div
        style={{
          display: "flex",
          justifyContent:
            "space-between",
          marginBottom: 12,
        }}
      >
        <strong>
          {sensor.sensor_id}
        </strong>

        <span>
          {status}
        </span>
      </div>

      <div
        style={{
          fontSize: 13,
          opacity: 0.75,
        }}
      >
        Station: {sensor.station_id}
      </div>

      <div
        style={{
          display: "grid",
          gridTemplateColumns:
            "1fr 1fr 1fr",
          gap: 8,
          marginTop: 16,
        }}
      >
        <div>
          <small>Temp</small>
          <br />
          {sensor.temperature_c ?? "--"} °C
        </div>

        <div>
          <small>Humidity</small>
          <br />
          {sensor.relative_humidity_pct ??
            "--"} %
        </div>

        <div>
          <small>Pressure</small>
          <br />
          {sensor.pressure_hpa ?? "--"}
        </div>
      </div>

      <div style={{ marginTop: 16 }}>
        <div
          style={{
            display: "flex",
            justifyContent:
              "space-between",
          }}
        >
          <span>Health</span>
          <strong>
            {health.toFixed(1)}
          </strong>
        </div>

        <div
          style={{
            height: 8,
            background: "#1b3425",
            borderRadius: 10,
            marginTop: 7,
          }}
        >
          <div
            style={{
              width: `${Math.max(
                0,
                Math.min(100, health)
              )}%`,
              height: "100%",
              background:
                health >= 70
                  ? "#4ade80"
                  : "#facc15",
              borderRadius: 10,
            }}
          />
        </div>
      </div>

      <div
        style={{
          marginTop: 14,
          fontSize: 13,
        }}
      >
        Latest anomaly:{" "}
        {sensor.latest_anomaly ??
          "None"}
      </div>

      <div
        style={{
          marginTop: 5,
          fontSize: 13,
          opacity: 0.8,
        }}
      >
        Confidence:{" "}
        {sensor.confidence ?? "--"}
      </div>
    </div>
  );
}