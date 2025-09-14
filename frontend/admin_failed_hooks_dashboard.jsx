import React, { useEffect, useState } from "react";
import AuditLogViewer from "./admin_audit_log.jsx";

const styles = {
  container: {
    padding: 24,
    maxWidth: 900,
    margin: '0 auto',
    fontFamily: 'Inter, Arial, sans-serif',
    background: '#f7f9fb',
    minHeight: '100vh',
  },
  table: {
    borderCollapse: 'collapse',
    width: '100%',
    marginTop: 16,
    background: '#fff',
    borderRadius: 8,
    overflow: 'hidden',
    boxShadow: '0 2px 8px #e3e3e3',
  },
  th: {
    background: '#2b4c7e',
    color: '#fff',
    padding: 12,
    textAlign: 'left',
    fontWeight: 600,
  },
  td: {
    padding: 10,
    borderBottom: '1px solid #e3e3e3',
    fontSize: 15,
    background: '#f9fbfd',
  },
  button: {
    marginTop: 24,
    background: '#2b4c7e',
    color: '#fff',
    padding: '10px 22px',
    border: 'none',
    borderRadius: 5,
    fontWeight: 600,
    fontSize: 16,
    cursor: 'pointer',
    boxShadow: '0 2px 6px #e3e3e3',
  },
  loginBox: {
    maxWidth: 340,
    margin: '60px auto',
    background: '#fff',
    borderRadius: 8,
    padding: 32,
    boxShadow: '0 2px 12px #e3e3e3',
    textAlign: 'center',
  },
  input: {
    width: '100%',
    padding: 10,
    margin: '10px 0',
    borderRadius: 4,
    border: '1px solid #ccc',
    fontSize: 16,
  },
  error: {
    color: '#b00020',
    margin: '10px 0',
    fontWeight: 500,
  },
  refresh: {
    marginLeft: 18,
    background: '#fff',
    color: '#2b4c7e',
    border: '1px solid #2b4c7e',
    fontWeight: 600,
    borderRadius: 5,
    padding: '10px 18px',
    cursor: 'pointer',
  },
};

function FailedHooksDashboard() {
  const [failedHooks, setFailedHooks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [jwt, setJwt] = useState("");
  const [loginState, setLoginState] = useState({ username: "", password: "" });
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [role, setRole] = useState("");
  const [error, setError] = useState(null);
  const [replayStatus, setReplayStatus] = useState(null);
  const [showAudit, setShowAudit] = useState(false);

  // JWT login flow
  const handleJWTLogin = async (e) => {
    e.preventDefault();
    setError(null);
    try {
      const res = await fetch("/api/token", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: `username=${encodeURIComponent(loginState.username)}&password=${encodeURIComponent(loginState.password)}`,
      });
      if (!res.ok) {
        setError("Login failed");
        return;
      }
      const data = await res.json();
      setJwt(data.access_token);
      // decode JWT to get role (not secure, but for UI only)
      const payload = JSON.parse(atob(data.access_token.split(".")[1]));
      setRole(payload.role || "viewer");
      setIsLoggedIn(true);
      fetchHooks(data.access_token);
    } catch {
      setError("Login failed");
    }
  };

  const fetchHooks = async (token) => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch("/api/failed_hooks", {
        headers: token ? { Authorization: `Bearer ${token}` } : {},
      });
      if (res.status === 401) {
        setIsLoggedIn(false);
        setError("Authentication failed.");
        setLoading(false);
        return;
      }
      const data = await res.json();
      setFailedHooks(data);
      setError(null);
    } catch (e) {
      setError("Failed to load hooks.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (jwt) fetchHooks(jwt);
    // eslint-disable-next-line
  }, [jwt]);

  const handleReplay = async () => {
    setReplayStatus("Running...");
    setError(null);
    const res = await fetch("/api/replay_failed_hooks", {
      method: "POST",
      headers: jwt ? { Authorization: `Bearer ${jwt}` } : {},
    });
    if (res.ok) {
      setReplayStatus("Replay triggered!");
      setTimeout(() => setReplayStatus(null), 2000);
      fetchHooks(jwt);
    } else if (res.status === 401 || res.status === 403) {
      setIsLoggedIn(false);
      setError("Authentication failed.");
      setReplayStatus(null);
    } else {
      setReplayStatus("Replay failed.");
    }
  };

  const handleRefresh = () => fetchHooks(jwt);

  if (!isLoggedIn) {
    return (
      <div style={styles.loginBox}>
        <h2>Admin Login</h2>
        <form onSubmit={handleJWTLogin}>
          <input
            style={styles.input}
            type="text"
            placeholder="Username"
            value={loginState.username}
            onChange={e => setLoginState({ ...loginState, username: e.target.value })}
            autoFocus
          />
          <input
            style={styles.input}
            type="password"
            placeholder="Password"
            value={loginState.password}
            onChange={e => setLoginState({ ...loginState, password: "YOUR_PASSWORD_HERE" })}
          />
          <button style={styles.button} type="submit">Login</button>
        </form>
        {error && <div style={styles.error}>{error}</div>}
      </div>
    );
  }

  return (
    <div style={styles.container}>
      <h2>Vault Management / Automation</h2>
      <div style={{ marginBottom: 32 }}>
        <h3>Failed Post-Sale Hooks</h3>
        <button style={styles.refresh} onClick={handleRefresh}>Refresh</button>
        {loading ? (
          <div>Loading...</div>
        ) : failedHooks.length === 0 ? (
          <div>No failed hooks 🎉</div>
        ) : (
          <table style={styles.table}>
            <thead>
              <tr>
                <th style={styles.th}>Timestamp</th>
                <th style={styles.th}>Hook</th>
                <th style={styles.th}>Error</th>
                <th style={styles.th}>Context</th>
              </tr>
            </thead>
            <tbody>
              {failedHooks.map((h, i) => (
                <tr key={i}>
                  <td style={styles.td}>{h.timestamp}</td>
                  <td style={styles.td}>{h.hook}</td>
                  <td style={styles.td}>{h.error}</td>
                  <td style={styles.td}>
                    <pre style={{ maxWidth: 400, overflowX: "auto" }}>{JSON.stringify(h.context, null, 2)}</pre>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
        <button style={styles.button} onClick={handleReplay} disabled={role !== "admin"}>
          Replay Failed Hooks
        </button>
        {replayStatus && <div style={{ marginTop: 8 }}>{replayStatus}</div>}
      </div>
      {/* Collapsible Audit Log Section */}
      <div style={{ marginBottom: 32 }}>
        <button
          style={{ ...styles.button, background: showAudit ? '#e3e3e3' : '#2b4c7e', color: showAudit ? '#2b4c7e' : '#fff', marginBottom: 12 }}
          onClick={() => setShowAudit(!showAudit)}
        >
          {showAudit ? 'Hide' : 'Show'} Audit Log
        </button>
        {showAudit && <AuditLogViewer token={jwt} />}
      </div>
    </div>
  );
}

      <div style={styles.loginBox}>
        <h2>Admin Login</h2>
        <form onSubmit={handleLogin}>
          <input
            style={styles.input}
            type="text"
            placeholder="Username"
            value={auth.user}
            onChange={e => setAuth({ ...auth, user: e.target.value })}
            autoFocus
          />
          <input
            style={styles.input}
            type="password"
            placeholder="Password"
            value={auth.pass}
            onChange={e => setAuth({ ...auth, pass: e.target.value })}
          />
          <button style={styles.button} type="submit">Login</button>
        </form>
        {error && <div style={styles.error}>{error}</div>}
      </div>
    );
  }

  return (
    <div style={styles.container}>
      <h2>Failed Post-Sale Hooks</h2>
      <button style={styles.refresh} onClick={handleRefresh}>Refresh</button>
      {loading ? (
        <div>Loading...</div>
      ) : failedHooks.length === 0 ? (
        <div>No failed hooks 🎉</div>
      ) : (
        <table style={styles.table}>
          <thead>
            <tr>
              <th style={styles.th}>Timestamp</th>
              <th style={styles.th}>Hook</th>
              <th style={styles.th}>Error</th>
              <th style={styles.th}>Context</th>
            </tr>
          </thead>
          <tbody>
            {failedHooks.map((h, i) => (
              <tr key={i}>
                <td style={styles.td}>{h.timestamp}</td>
                <td style={styles.td}>{h.hook}</td>
                <td style={styles.td}>{h.error}</td>
                <td style={styles.td}>
                  <pre style={{ maxWidth: 400, overflowX: "auto" }}>{JSON.stringify(h.context, null, 2)}</pre>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
      <button style={styles.button} onClick={handleReplay}>
        Replay Failed Hooks
      </button>
      {replayStatus && <div style={{ marginTop: 8 }}>{replayStatus}</div>}
    </div>
  );
}

export default FailedHooksDashboard;
