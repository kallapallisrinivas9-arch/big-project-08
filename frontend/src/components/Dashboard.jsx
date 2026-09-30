import React, {
  useEffect,
  useMemo,
  useState,
} from "react";

import AlertPanel from "./AlertPanel";
import AnomalyTable from "./AnomalyTable";
import HealthChart from "./HealthChart";
import SensorCard from "./SensorCard";


const API =
  import.meta.env.VITE_API_URL ||
  "http://127.0.0.1:8000";


export default function Dashboard() {

  const [data, setData] = useState({
    observations: [],
    anomalies: [],
    alerts: [],
    sensor_health: [],
  });

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState("");


  async function request(path) {

    const response = await fetch(
      `${API}${path}`
    );

    if (!response.ok) {
      throw new Error(
        `API error: ${response.status}`
      );
    }

    const body =
      await response.json();

    if (!body.success) {
      throw new Error(
        body.error ||
        "API request failed"
      );
    }

    return body.data;
  }


  async function loadDashboard() {

    try {

      setLoading(true);
      setError("");

      const [
        observations,
        anomalies,
        alerts,
        sensorHealth,
      ] = await Promise.all([
        request("/observations"),
        request("/anomalies"),
        request("/alerts"),
        request(
          "/sensor-health"
        ),
      ]);

      setData({
        observations:
          observations || [],
        anomalies:
          anomalies || [],
        alerts:
          alerts || [],
        sensor_health:
          sensorHealth || [],
      });

    } catch (err) {

      setError(
        err.message ||
        "Unable to connect to backend."
      );
    } finally {
      setLoading(false);
    }
  }


  async function runSimulation() {

    try {

      setLoading(true);
      setError("");

      const response =
        await fetch(
          `${API}/simulate`,
          {
            method: "POST",
            headers: {
              "Content-Type":
                "application/json",
            },
            body: JSON.stringify({
              stations: 4,
              records_per_station: 120,
              seed: 42,
              inject_faults: true,
            }),
          }
        );

      const body =
        await response.json();

      if (!body.success) {
        throw new Error(
          body.error ||
          "Simulation failed."
        );
      }

      const result =
        body.data;

      setData({
        observations:
          result.observations ||
          [],
        anomalies:
          result.anomalies ||
          [],
        alerts:
          result.alerts ||
          [],
        sensor_health:
          result.sensor_health ||
          [],
      });

    } catch (err) {

      setError(
        err.message ||
        "Simulation failed."
      );

    } finally {
      setLoading(false);
    }
  }


  useEffect(() => {
    loadDashboard();
  }, []);


  const sensorCards =
    useMemo(() => {

      const latest = {};

      for (
        const observation of
        data.observations
      ) {

        latest[
          observation.sensor_id
        ] = observation;
      }

      return data.sensor_health.map(
        (health) => {

          const observation =
            latest[
              health.sensor_id
            ];

          const anomaly =
            [...data.anomalies]
              .reverse()
              .find(
                (item) =>
                  item.sensor_id ===
                  health.sensor_id
              );

          return {
            ...health,
            ...observation,
            latest_anomaly:
              anomaly?.root_cause ??
              "None",
            confidence:
              anomaly?.confidence ??
              "--",
          };
        }
      );

    }, [data]);


  const totalStations =
    new Set(
      data.observations.map(
        (item) =>
          item.station_id
      )
    ).size;


  const totalSensors =
    data.sensor_health.length;


  const faultySensors =
    data.sensor_health.filter(
      (item) =>
        item.status !== "HEALTHY"
    ).length;


  const normalSensors =
    Math.max(
      0,
      totalSensors -
      faultySensors
    );


  const activeAnomalies =
    data.anomalies.filter(
      (item) =>
        item.anomaly_flag
    ).length;


  const criticalAlerts =
    data.alerts.filter(
      (item) =>
        item.severity ===
        "CRITICAL"
    ).length;


  return (
    <div
      style={{
        maxWidth: 1450,
        margin: "0 auto",
        padding: 24,
      }}
    >

      <header
        style={{
          display: "flex",
          justifyContent:
            "space-between",
          alignItems: "center",
          gap: 15,
          flexWrap: "wrap",
        }}
      >

        <div>
          <div
            style={{
              fontSize: 13,
              opacity: 0.7,
            }}
          >
            SIH 2026 • SIH26073
          </div>

          <h1
            style={{
              margin:
                "5px 0",
              fontSize: 32,
            }}
          >
            WeatherGuard AI
          </h1>

          <div
            style={{
              opacity: 0.75,
            }}
          >
            Intelligent AWS Anomaly
            Detection & Sensor Health
          </div>
        </div>

        <button
          onClick={runSimulation}
          disabled={loading}
          style={{
            border: "none",
            borderRadius: 10,
            padding:
              "12px 20px",
            background:
              "#4ade80",
            color: "#06120a",
            fontWeight: 700,
            cursor: "pointer",
          }}
        >
          {loading
            ? "Running AI..."
            : "Run AI Simulation"}
        </button>

      </header>


      {error && (
        <div
          style={{
            marginTop: 20,
            padding: 14,
            borderRadius: 10,
            background:
              "#3b1518",
            border:
              "1px solid #7f1d1d",
          }}
        >
          {error}
        </div>
      )}

      {!loading &&
        !error &&
        data.observations.length === 0 && (
          <section
            style={{
              marginTop: 25,
              padding: 28,
              textAlign: "center",
              background: "#102219",
              border: "1px solid #274634",
              borderRadius: 14,
            }}
          >
            <h2>Ready for a sensor health check</h2>
            <p style={{ opacity: 0.75 }}>
              Run the synthetic AWS scenario to populate the dashboard
              with observations, anomalies, and alerts.
            </p>
            <button
              onClick={runSimulation}
              style={{
                border: "none",
                borderRadius: 10,
                padding: "12px 20px",
                background: "#4ade80",
                color: "#06120a",
                fontWeight: 700,
                cursor: "pointer",
              }}
            >
              Run AI Simulation
            </button>
          </section>
        )}


      <section
        style={{
          display: "grid",
          gridTemplateColumns:
            "repeat(auto-fit, minmax(160px, 1fr))",
          gap: 14,
          marginTop: 25,
        }}
      >

        {[
          [
            "Stations",
            totalStations,
          ],
          [
            "Sensors",
            totalSensors,
          ],
          [
            "Normal Sensors",
            normalSensors,
          ],
          [
            "Faulty Sensors",
            faultySensors,
          ],
          [
            "Active Anomalies",
            activeAnomalies,
          ],
          [
            "Critical Alerts",
            criticalAlerts,
          ],
        ].map(
          ([title, value]) => (
            <div
              key={title}
              style={{
                background:
                  "#102219",
                border:
                  "1px solid #274634",
                borderRadius: 14,
                padding: 18,
              }}
            >
              <div
                style={{
                  fontSize: 13,
                  opacity: 0.7,
                }}
              >
                {title}
              </div>

              <div
                style={{
                  fontSize: 30,
                  fontWeight: 800,
                  marginTop: 7,
                }}
              >
                {value}
              </div>
            </div>
          )
        )}

      </section>


      <section
        style={{
          marginTop: 25,
          background:
            "#0d1c13",
          border:
            "1px solid #274634",
          borderRadius: 14,
          padding: 18,
        }}
      >

        <h2>
          Sensor Monitoring
        </h2>

        <div
          style={{
            display: "grid",
            gridTemplateColumns:
              "repeat(auto-fit, minmax(250px, 1fr))",
            gap: 15,
          }}
        >

          {sensorCards.map(
            (sensor) => (
              <SensorCard
                key={
                  sensor.sensor_id
                }
                sensor={sensor}
              />
            )
          )}

        </div>

      </section>


      <section
        style={{
          display: "grid",
          gridTemplateColumns:
            "minmax(0, 2fr) minmax(300px, 1fr)",
          gap: 20,
          marginTop: 20,
        }}
      >

        <div
          style={{
            background:
              "#0d1c13",
            border:
              "1px solid #274634",
            borderRadius: 14,
            padding: 18,
          }}
        >

          <h2>
            Recent Anomalies
          </h2>

          <AnomalyTable
            anomalies={
              data.anomalies
                .filter(
                  (item) =>
                    item.anomaly_flag
                )
                .slice(-20)
            }
          />

        </div>


        <div
          style={{
            background:
              "#0d1c13",
            border:
              "1px solid #274634",
            borderRadius: 14,
            padding: 18,
          }}
        >

          <h2>
            Sensor Health
          </h2>

          <HealthChart
            health={
              data.sensor_health
            }
          />

        </div>

      </section>


      <section
        style={{
          marginTop: 20,
          background:
            "#0d1c13",
          border:
            "1px solid #274634",
          borderRadius: 14,
          padding: 18,
        }}
      >

        <h2>
          Alerts
        </h2>

        <AlertPanel
          alerts={
            data.alerts
          }
        />

      </section>


      <section
        style={{
          marginTop: 20,
          padding: 20,
          borderRadius: 14,
          background:
            "#102219",
          border:
            "1px solid #274634",
        }}
      >

        <h2>
          How WeatherGuard AI Works
        </h2>

        <p
          style={{
            lineHeight: 1.7,
            opacity: 0.85,
          }}
        >
          AWS Data → Validation →
          Feature Engineering →
          Physics & Statistical Checks
          → Isolation Forest →
          Evidence Fusion →
          Root Cause →
          Confidence →
          Correction Decision →
          Sensor Health →
          Alerts
        </p>

      </section>

    </div>
  );
}