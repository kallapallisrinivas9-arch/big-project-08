import React from "react";

export default function AlertPanel({
  alerts = [],
}) {
  return (
    <div
      style={{
        display: "grid",
        gap: 10,
      }}
    >
      {alerts.length === 0 && (
        <div
          style={{
            padding: 15,
            opacity: 0.7,
          }}
        >
          No active alerts.
        </div>
      )}

      {alerts.map(
        (alert, index) => (
          <div
            key={index}
            style={{
              background:
                "#1b241b",
              border:
                "1px solid #4a593f",
              borderRadius: 10,
              padding: 14,
            }}
          >
            <div
              style={{
                display: "flex",
                justifyContent:
                  "space-between",
              }}
            >
              <strong>
                {alert.alert_type}
              </strong>

              <span>
                {alert.severity}
              </span>
            </div>

            <div
              style={{
                marginTop: 6,
                fontSize: 13,
              }}
            >
              {alert.station_id} /{" "}
              {alert.sensor_id}
            </div>

            <div
              style={{
                marginTop: 8,
              }}
            >
              {alert.message}
            </div>

            <div
              style={{
                marginTop: 8,
                fontSize: 12,
                opacity: 0.7,
              }}
            >
              {alert.timestamp
                ? new Date(
                    alert.timestamp
                  ).toLocaleString()
                : "--"}
              {" • "}
              {alert.status}
            </div>
          </div>
        )
      )}
    </div>
  );
}