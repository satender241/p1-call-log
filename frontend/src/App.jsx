// The DINING ROOM: the page people see. It never touches the database.
// It only asks the API (the waiter) for the calls, then draws one line per call.
import { useEffect, useState } from "react";

// Where the API lives. On your laptop this comes from frontend/.env,
// and on Vercel from the "Environment Variables" settings page.
const API_URL = import.meta.env.VITE_API_URL;

export default function App() {
  const [calls, setCalls] = useState([]); // the list of calls we show
  const [status, setStatus] = useState("loading"); // "loading", "ready" or "error"
  const [error, setError] = useState("");

  async function loadCalls() {
    setStatus("loading");
    try {
      if (!API_URL) throw new Error("VITE_API_URL is not set, so the page doesn't know where the API is.");
      const reply = await fetch(`${API_URL}/calls`); // GET /calls: ask the waiter for the calls
      if (!reply.ok) throw new Error(`The API replied with status ${reply.status}.`);
      setCalls(await reply.json()); // the JSON list from the backend
      setStatus("ready");
    } catch (err) {
      setError(err.message);
      setStatus("error");
    }
  }

  // Run loadCalls once, when the page first opens.
  useEffect(() => {
    loadCalls();
  }, []);

  return (
    <main>
      <header>
        <h1>My Call Log</h1>
        <button onClick={loadCalls} disabled={status === "loading"}>
          {status === "loading" ? "Loading…" : "Refresh"}
        </button>
      </header>

      {status === "loading" && (
        <p className="note">
          Asking the API for calls… The free Render server sleeps when nobody uses it, so the first load can
          take up to a minute.
        </p>
      )}

      {status === "error" && (
        <p className="note error">
          Couldn’t load the calls. {error} (API address: {API_URL || "not set"})
        </p>
      )}

      {status === "ready" && calls.length === 0 && (
        <p className="note">No calls yet. Add one with curl or Postman, then press Refresh.</p>
      )}

      {/* For every call, draw one row. This is the same line as on the training slide. */}
      <ul>
        {calls.map((call) => (
          <li key={call.id}>
            <div className="row-top">
              <strong>{call.caller}</strong>
              <span className="meta">
                #{call.id} · {new Date(call.created_at).toLocaleString("en-IN", { dateStyle: "medium", timeStyle: "short" })}
              </span>
            </div>
            <p>{call.summary}</p>
          </li>
        ))}
      </ul>
    </main>
  );
}
