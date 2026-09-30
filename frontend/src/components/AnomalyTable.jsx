import React from "react";

export default function AnomalyTable({
  anomalies = [],
}) {
  return (
    <div
      style={{
        overflowX: "auto",
      }}
    >
      <table
        style={{
          width: "100%",
          borderCollapse:
            "collapse",
          fontSize: 13,
        }}
      >
        <thead>
          <tr>
            {[
              "Time",
              "Station",
              "Sensor",
              "Score",
              "Root Cause",
              "Decision",
              "Confidence",
              "Explanation",
            ].map((heading) => (
              <th
                key={heading}
                style={{
                  textAlign: "left",
                  padding: 10,
                  borderBottom:
                    "1px solid #294636",
                }}
              >
                {heading}
              </th>
            ))}
          </tr>
        </thead>

        <tbody>
          {anomalies.map(
            (item, index) => (
              <tr
                key={
                  item.observation_id ??
                  index
                }
              >
                <td style={{ padding: 10 }}>
                  {item.observed_at
                    ? new Date(
                        item.observed_at
                      ).toLocaleString()
                    : "--"}
                </td>

                <td style={{ padding: 10 }}>
                  {item.station_id}
                </td>

                <td style={{ padding: 10 }}>
                  {item.sensor_id}
                </td>

                <td style={{ padding: 10 }}>
                  {Number(
                    item.anomaly_score ??
                      0
                  ).toFixed(3)}
                </td>

                <td style={{ padding: 10 }}>
                  {item.root_cause}
                </td>

                <td style={{ padding: 10 }}>
                  {item.correction
                    ?.decision ?? "--"}
                </td>

                <td style={{ padding: 10 }}>
                  {item.confidence}
                </td>

                <td style={{ padding: 10 }}>
                  {item.explanation}
                </td>
              </tr>
            )
          )}
        </tbody>
      </table>

      {anomalies.length === 0 && (
        <div
          style={{
            padding: 20,
            opacity: 0.7,
          }}
        >
          No anomalies detected.
        </div>
      )}
    </div>
  );
}