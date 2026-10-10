import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Legend
} from "recharts";

import { useEffect, useState } from "react";
import "./App.css";
import MapView from "./components/MapView";
import WeatherAlerts from "./components/WeatherAlerts";
export default function App() {
  const getPriorityColor = (priority) => {
    switch (priority?.toLowerCase()) {
      case "critical":
        return "#dc2626";
      case "high":
        return "#ea580c";
      case "medium":
        return "#eab308";
      case "low":
        return "#16a34a";
      default:
        return "#2563eb";
    }
  };

  const [emergency, setEmergency] = useState("");
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [search, setSearch] = useState("");

  const total = history.length;

  const high = history.filter(
    (e) => e.priority?.toLowerCase() === "high"
  ).length;

  const medium = history.filter(
    (e) => e.priority?.toLowerCase() === "medium"
  ).length;

  const low = history.filter(
    (e) => e.priority?.toLowerCase() === "low"
  ).length;

  const priorityData = [
    { name: "High", value: high },
    { name: "Medium", value: medium },
    { name: "Low", value: low }
  ];

  const typeData = {};

  history.forEach((item) => {
    if (item.emergency_type) {
      typeData[item.emergency_type] =
        (typeData[item.emergency_type] || 0) + 1;
    }
  });

  const emergencyTypeData = Object.keys(typeData).map((key) => ({
    name: key,
    value: typeData[key]
  }));

  const filteredHistory = history.filter(
    (item) =>
      item.emergency_type?.toLowerCase().includes(search.toLowerCase()) ||
      item.priority?.toLowerCase().includes(search.toLowerCase()) ||
      item.summary?.toLowerCase().includes(search.toLowerCase())
  );

  const COLORS = [
    "#ef4444",
    "#f59e0b",
    "#10b981",
    "#3b82f6",
    "#8b5cf6",
    "#ec4899"
  ];

  async function loadHistory() {
    const response = await fetch("http://127.0.0.1:8000/history");
    const data = await response.json();
    setHistory(data);
  }

  async function analyze() {
    const response = await fetch(
      `http://127.0.0.1:8000/analyze?emergency=${encodeURIComponent(
        emergency
      )}`
    );

    const data = await response.json();

    setResult(data);

    loadHistory();
  }

  useEffect(() => {
    loadHistory();
  }, []);

  return (
    <div className="container">
      <h1>🚨 AI Emergency Response Coordinator</h1>
      <WeatherAlerts />

      <textarea
        rows="5"
        value={emergency}
        onChange={(e) => setEmergency(e.target.value)}
        placeholder="Describe the emergency..."
      />

      <button onClick={analyze}>Analyze Emergency</button>

      <div className="stats">
        <div className="stat-card">
          <h3>Total</h3>
          <h2>{total}</h2>
        </div>

        <div className="stat-card">
          <h3>High</h3>
          <h2>{high}</h2>
        </div>

        <div className="stat-card">
          <h3>Medium</h3>
          <h2>{medium}</h2>
        </div>

        <div className="stat-card">
          <h3>Low</h3>
          <h2>{low}</h2>
        </div>
      </div>

      {result && (
        <div className="card">
          <h2>Emergency Report</h2>

          <div className="grid">
            <div className="info-box">
              <h3>Priority</h3>
              <p
                style={{
                  color: getPriorityColor(result.priority),
                  fontWeight: "bold",
                  fontSize: "20px"
                }}
              >
                {result.priority}
              </p>
            </div>

            <div className="info-box">
              <h3>Emergency</h3>
              <p>{result.emergency_type}</p>
            </div>

            <div className="info-box">
              <h3>Location</h3>
              <p>{result.location?.city || "Unknown"}</p>
            </div>

            <div className="info-box">
              <h3>Confidence</h3>
              <div className="progress-bar">
                <div
                  className="progress-fill"
                  style={{ width: `${result.confidence}%` }}
                ></div>
              </div>
              <p>{result.confidence}%</p>
            </div>

            <div className="info-box">
              <h3>Response Time</h3>
              <p>{result.estimated_response_time}</p>
            </div>
          </div>

          <h2 style={{ marginTop: "30px" }}>Emergency Services</h2>

          <div className="services">
            {result.agents?.ambulance && (
    <div className="service-card">
        <h3>🚑 Ambulance</h3>

        <p>
            <strong>
                {result.agents.ambulance.ambulance_required
                    ? "Ambulance Required"
                    : "Ambulance Not Required"}
            </strong>
        </p>

        <p>
            <strong>Priority:</strong>{" "}
            {result.agents.ambulance.priority}
        </p>

        <p>
            <strong>Reason:</strong>{" "}
            {result.agents.ambulance.reason}
        </p>

        <p>
            <strong>Response Time:</strong>{" "}
            {result.agents.ambulance.response_time}
        </p>
    </div>
)}
            {result.agents?.police && (
              <div className="service-card">
                <h3>🚓 Police</h3>
                <p>{result.agents.police.status}</p>
              </div>
            )}

            {result.agents?.fire && (
              <div className="service-card">
                <h3>🚒 Fire</h3>
                <p>{result.agents.fire.status}</p>
              </div>
            )}

            {result.agents?.hospital && (
              <div className="service-card">
                <h3>🏥 Hospital</h3>

                <p>
                  <strong>{result.agents.hospital.hospital_name}</strong>
                </p>

                <p>{result.agents?.hospital?.department}</p>

                <p>{result.agents?.hospital?.phone}</p>
              </div>
            )}
          </div>

          <h2 style={{ marginTop: "30px" }}>Hospital Location</h2>
          <MapView />
        </div>
      )}

      <h2 style={{ marginTop: "40px" }}>Emergency History</h2>

      <input
        type="text"
        placeholder="🔍 Search by emergency type, priority, or summary..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        className="search-box"
      />

      <table className="history-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Type</th>
            <th>Priority</th>
            <th>Confidence</th>
          </tr>
        </thead>

        <tbody>
          {filteredHistory.map((item) => (
            <tr key={item.id}>
              <td>{item.id}</td>
              <td>{item.emergency_type}</td>
              <td>{item.priority}</td>
              <td>{item.confidence}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <h2 style={{ marginTop: "40px" }}>Analytics</h2>

      <div className="charts">
        <div className="chart-card">
          <h3>Priority Distribution</h3>

          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={priorityData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="value" fill="#2563eb" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="chart-card">
          <h3>Emergency Types</h3>

          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={emergencyTypeData}
                dataKey="value"
                nameKey="name"
                outerRadius={100}
                label
              >
                {emergencyTypeData.map((entry, index) => (
                  <Cell
                    key={index}
                    fill={COLORS[index % COLORS.length]}
                  />
                ))}
              </Pie>

              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}