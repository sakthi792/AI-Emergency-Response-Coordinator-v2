
import { useEffect, useRef, useState } from "react";

const API = "http://127.0.0.1:8000";

export default function WeatherAlerts() {
  const [alerts, setAlerts] = useState([]);
  const [status, setStatus] = useState("Loading alerts...");
  const [permission, setPermission] = useState(
    typeof Notification === "undefined"
      ? "unsupported"
      : Notification.permission
  );

  const seenAlerts = useRef(new Set());

  async function requestNotifications() {
    if (!("Notification" in window)) {
      setPermission("unsupported");
      return;
    }

    const result = await Notification.requestPermission();
    setPermission(result);
  }

  useEffect(() => {
    let cancelled = false;

    async function checkAlerts() {
      try {
        const response = await fetch(`${API}/alerts/weather`);
        if (!response.ok) throw new Error("API unavailable");

        const data = await response.json();
        if (cancelled) return;

        if (data.status !== "source_available") {
          setStatus("Weather alerts could not be verified.");
          return;
        }

        const items = Array.isArray(data.alerts) ? data.alerts : [];
        setAlerts(items);
        setStatus(`Source checked: ${data.checked_at}`);

        // Alert fields vary by source. Avoid guessing that
        // every raw record is a confirmed dangerous warning.
        for (const item of items) {
          const severity = String(
            item.severity ?? item.warning_level ?? ""
          ).toLowerCase();

          const message = String(
            item.warning ?? item.warning_text ?? item.description ?? ""
          );

          const id = String(
            item.id ?? item.district_id ?? `${severity}:${message}`
          );

          const dangerous =
            /red|orange|severe|extremely heavy|very heavy|cyclone|warning/i
              .test(`${severity} ${message}`);

          if (
            dangerous &&
            message &&
            !seenAlerts.current.has(id)
          ) {
            seenAlerts.current.add(id);

            if (
              Notification.permission === "granted"
            ) {
              new Notification("Weather alert — verify official bulletin", {
                body: message.slice(0, 220),
                tag: id,
              });
            }
          }
        }
      } catch {
        if (!cancelled) {
          setStatus("Unable to verify current weather alerts.");
        }
      }
    }

    checkAlerts();
    const timer = setInterval(checkAlerts, 5 * 60 * 1000);

    return () => {
      cancelled = true;
      clearInterval(timer);
    };
  }, []);

  return (
    <section className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
      <h2 className="text-xl font-bold">
        Weather & Disaster Alerts
      </h2>

      <p className="mt-2 text-sm text-slate-600">
        India · {status}
      </p>

      <button
        onClick={requestNotifications}
        className="mt-4 rounded-lg bg-blue-600 px-4 py-2 text-white"
      >
        {permission === "granted"
          ? "Browser notifications enabled"
          : "Enable browser notifications"}
      </button>

      <p className="mt-2 text-xs text-slate-500">
        Automatic checks run every 5 minutes while this page is open.
      </p>

      <div className="mt-4 space-y-3">
        {alerts.length === 0 ? (
          <p className="text-sm text-slate-600">
            No alert records returned. This does not confirm that
            there is no danger.
          </p>
        ) : (
          alerts.map((item, index) => (
            <article
              key={item.id ?? index}
              className="rounded-lg border border-slate-200 p-3"
            >
              <p className="font-semibold">
                {item.district_name ??
                  item.district ??
                  item.name ??
                  "Weather warning"}
              </p>
              <p className="mt-1 text-sm">
                {item.warning ??
                  item.warning_text ??
                  item.description ??
                  JSON.stringify(item)}
              </p>
            </article>
          ))
        )}
      </div>

      <a
        href="https://tsunami.incois.gov.in/TEWS/searlywarnings.jsp"
        target="_blank"
        rel="noreferrer"
        className="mt-5 inline-block text-blue-700 underline"
      >
        Check official INCOIS tsunami warnings
      </a>
    </section>
  );
}
