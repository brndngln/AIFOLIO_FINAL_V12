import React, { useRef } from "react";

function getSettings() {
  return {
    brand: JSON.parse(localStorage.getItem("aifolio_brand") || "{}"),
    onboarding: JSON.parse(
      localStorage.getItem("aifolio_onboarding_progress") || "[]",
    ),
    accessibility: JSON.parse(
      localStorage.getItem("aifolio_accessibility_progress") || "[]",
    ),
    demo: localStorage.getItem("aifolio_demo_mode") === "true",
  };
}

function setSettings(settings) {
  if (settings.brand)
    localStorage.setItem("aifolio_brand", JSON.stringify(settings.brand));
  if (settings.onboarding)
    localStorage.setItem(
      "aifolio_onboarding_progress",
      JSON.stringify(settings.onboarding),
    );
  if (settings.accessibility)
    localStorage.setItem(
      "aifolio_accessibility_progress",
      JSON.stringify(settings.accessibility),
    );
  if (typeof settings.demo === "boolean")
    localStorage.setItem("aifolio_demo_mode", settings.demo ? "true" : "false");
}

// [WINDSURF FIXED ✅]
export default function OwnerBackupRestorePanel() {
  const inputRef = useRef(); // Remove if not used in render or logic

  function handleBackup() {
    const data = JSON.stringify(getSettings(), null, 2);
    const blob = new Blob([data], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `AIFOLIO_OWNER_BACKUP_${new Date().toISOString().slice(0, 10)}.json`;
    document.body.appendChild(a);
    a.click();
    setTimeout(() => {
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }, 1000);
  }

  function handleRestore(e) {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = () => {
      try {
        const settings = JSON.parse(reader.result);
        setSettings(settings);
        alert("OWNER settings restored! Reload the page to apply changes.");
      } catch {
        alert("Invalid backup file.");
      }
    };
    reader.readAsText(file);
  }

  return (
    <section
      aria-labelledby="backup-restore-heading"
      style={{
        background: "#f9fafb",
        borderRadius: 12,
        padding: 32,
        marginBottom: 32,
        boxShadow: "0 2px 8px #e0e7ef",
      }}
    >
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 10,
          marginBottom: 12,
        }}
      >
        <h2
          id="backup-restore-heading"
          style={{ color: "#0ea5e9", fontWeight: 800, fontSize: 22, margin: 0 }}
        >
          OWNER Backup & Restore
        </h2>
        <span
          style={{
            background: "#0ea5e9",
            color: "#fff",
            padding: "2px 10px",
            borderRadius: 6,
            fontWeight: 700,
            fontSize: 13,
          }}
          aria-label="OWNER badge"
        >
          OWNER
        </span>
        <span
          tabIndex={0}
          aria-label="Help: Backup & Restore"
          title="Export all OWNER settings as JSON or restore from a backup file. Static, browser-only."
          style={{
            marginLeft: 6,
            color: "#64748b",
            cursor: "help",
            fontSize: 18,
            fontWeight: 800,
          }}
        >
          ?
        </span>
      </div>
      <div
        style={{
          display: "flex",
          gap: 24,
          alignItems: "center",
          marginBottom: 18,
        }}
      >
        <button
          style={{
            background: "#0ea5e9",
            color: "#fff",
            border: "none",
            borderRadius: 6,
            padding: "10px 20px",
            fontWeight: 700,
            fontSize: 15,
            cursor: "pointer",
            boxShadow: "0 1px 2px #bae6fd",
          }}
          aria-label="Export OWNER settings as JSON"
          onClick={handleBackup}
        >
          Backup OWNER Settings
        </button>
        <label style={{ fontWeight: 600 }}>
          Restore from Backup
          <input
            ref={inputRef}
            type="file"
            accept="application/json"
            style={{ marginLeft: 10 }}
            aria-label="Restore OWNER settings from backup file"
            onChange={handleRestore}
          />
        </label>
      </div>
      <div style={{ marginTop: 10, color: "#64748b", fontSize: 13 }}>
        <b>OWNER CONTROLLED:</b> Backup/restore is static and browser-only. No
        server or adaptive logic.
      </div>
    </section>
  );
}
