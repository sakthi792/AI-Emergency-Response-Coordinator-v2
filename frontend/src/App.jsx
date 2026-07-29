import { useState, useEffect } from "react";
import "./App.css";

function App() {
  const [emergency, setEmergency] = useState("");
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  const loadHistory = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/history");
      const data = await response.json();
      setHistory(data);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    loadHistory();
  }, []);

  const analyzeEmergency = async () => {
    if (!emergency.trim()) {
      alert("Please enter an emergency.");
      return;
    }

    try {
      setLoading(true);

      const response = await fetch(
        `http://127.0.0.1:8000/analyze?emergency=${encodeURIComponent(emergency)}`
      );

      const data = await response.json();

      setResult(data);

      loadHistory();
    } catch (error) {
      console.error(error);

      setResult({
        error: "Failed to connect to backend.",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <div className="card">
        <h1>
          🚨 AI Emergency
          <br />
          Response Coordinator
        </h1>

        <textarea
          rows="6"
          value={emergency}
          onChange={(e) => setEmergency(e.target.value)}
          placeholder="Describe the emergency..."
          className="textarea"
        />

        <button
          onClick={analyzeEmergency}
          className="button"
          disabled={loading}
        >
          {loading ? "⏳ Analyzing Emergency..." : "🚨 Analyze Emergency"}
        </button>

        {result && result.error && (
          <div className="result-card">
            <h2>❌ Error</h2>
            <p>{result.error}</p>
          </div>
        )}

        {result && !result.error && (
          <div className="result-card">
            <h2>🚨 Emergency Analysis</h2>

            <div className="info-row">
              <strong>Priority</strong>
              <span>{result.priority}</span>
            </div>

            <div className="info-row">
              <strong>Confidence</strong>
              <span>{result.confidence}</span>
            </div>

            <div className="info-row">
              <strong>Emergency Type</strong>
              <span>{result.emergency_type}</span>
            </div>

            <div className="info-row">
              <strong>Summary</strong>
              <span>{result.summary}</span>
            </div>

            <div className="info-row">
              <strong>Ambulance</strong>
              <span>
                {result.ambulance_required
                  ? "✅ Required"
                  : "❌ Not Required"}
              </span>
            </div>

            <div className="info-row">
              <strong>Estimated Response Time</strong>
              <span>{result.estimated_response_time}</span>
            </div>

            <h3>🏥 Hospital Departments</h3>

            <ul>
              {result.hospital_department?.map((dept, index) => (
                <li key={index}>{dept}</li>
              ))}
            </ul>

            <h3>🩹 First Aid Steps</h3>

            <ul>
              {result.first_aid?.map((item, index) => (
                <li key={index}>{item}</li>
              ))}
            </ul>

            <h3>🚑 Recommended Action</h3>

            <p>{result.recommended_action}</p>

            <h3>💡 Reason</h3>

            <p>{result.reason}</p>
          </div>
        )}

        <div className="result-card">
          <h2>📜 Emergency History</h2>

          {history.length === 0 ? (
            <p>No emergency history found.</p>
          ) : (
            <table className="history-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Emergency</th>
                  <th>Priority</th>
                  <th>Confidence</th>
                  <th>Ambulance</th>
                </tr>
              </thead>

              <tbody>
                {history.map((item) => (
                  <tr key={item.id}>
                    <td>{item.id}</td>
                    <td>{item.emergency_type}</td>
                    <td>{item.priority}</td>
                    <td>{item.confidence}</td>
                    <td>
                      {item.ambulance_required ? "✅ Yes" : "❌ No"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;