import React from "react";

export default function HealthChart({
  health = [],
}) {
  return (
    <div
      style={{
        display: "grid",
        gap: 14,
      }}
    >
      {health.map((item) => {
        const score = Number(
          item.health_score ?? 0
        );

        return (
          <div
            key={
              item.sensor_id
            }
          >
            <div
              style={{
                display: "flex",
                justifyContent:
                  "space-between",
                fontSize: 13,
              }}
            >
              <span>
                {item.sensor_id}
              </span>

              <strong>
                {score.toFixed(1)}
              </strong>
            </div>

            <div
              style={{
                height: 10,
                background:
                  "#20392a",
                borderRadius: 10,
                marginTop: 5,
              }}
            >
              <div
                style={{
                  height: "100%",
                  width: `${Math.min(
                    100,
                    Math.max(0, score)
                  )}%`,
                  background:
                    score >= 85
                      ? "#4ade80"
                      : score >= 65
                      ? "#facc15"
                      : "#fb7185",
                  borderRadius: 10,
                }}
              />
            </div>

            <div
              style={{
                fontSize: 11,
                opacity: 0.65,
                marginTop: 4,
              }}
            >
              {item.status} •{" "}
              {item.trend} • Risk:{" "}
              {item.maintenance_risk}
            </div>
          </div>
        );
      })}
    </div>
  );
}