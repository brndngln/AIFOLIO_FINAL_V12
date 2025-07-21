import React, { useState, useEffect } from "react";
import {
  Switch,
  FormControlLabel,
  Tooltip,
  Button,
  MenuItem,
  Select,
  InputLabel,
  TextField,
} from "@mui/material";

const biometricTypes = ["face", "retina", "fingerprint", "voiceprint"];
const approvalModes = [
  { value: "full_lockdown", label: "Full Auto-Lockdown" },
  { value: "delayed_review", label: "Delayed Review" },
  { value: "passive_oversight", label: "Passive Oversight" },
];
const notificationTypes = [
  "Urgent",
  "Legal",
  "Business",
  "AI Behavior",
  "Personal",
  "Reminder",
];
const notificationFrequencies = ["Immediate", "Hourly Digest", "Daily Digest"];
const notificationFormats = [
  "Voice",
  "Visual UI",
  "Email",
  "Telegram",
  "PDF Summary",
];
const authorityLevels = ["Needs Approval", "Passive Log Only", "Auto-Execute"];

export default function IntegrationControls({
  notificationPrefs,
  onPrefsChange,
  onRotateApiKey,
  onComplianceAudit,
}) {
  // Biometric
  const [biometricStatus, setBiometricStatus] = useState(""); // Remove if not used in render or logic
  // Approval Mode
  const [approvalMode, setApprovalMode] = useState("full_lockdown");
  useEffect(() => {
    fetch("/api/owner/approval-mode", { credentials: "include" })
      .then((r) => (r.ok ? r.json() : { mode: "full_lockdown" }))
      .then((d) => setApprovalMode(d.mode));
  }, []);
  const handleSetApprovalMode = async (mode) => {
    setApprovalMode(mode);
    await fetch("/api/owner/approval-mode", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify(mode),
    });
  };
  // Legal Sentinel
  const [emmaStatus, setEmmaStatus] = useState(null);
  const [contractText, setContractText] = useState("");
  const [contractReview, setContractReview] = useState("");
  const handleLegalScan = async () => {
    const res = await fetch("/api/owner/legal-contract-scan", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify(contractText),
    });
    if (res.ok) {
      const data = await res.json();
      setContractReview(data.recommendations.join(" "));
    }
  };
  useEffect(() => {
    fetch("/api/owner/legal-sentinel-status", { credentials: "include" })
      .then((r) => (r.ok ? r.json() : null))
      .then(setEmmaStatus);
  }, []);
  // Anti-Sentience
  const [watchdogStatus, setWatchdogStatus] = useState("");
  const handleWatchdogScan = async () => {
    const res = await fetch("/api/owner/anti-sentience-scan", {
      method: "POST",
      credentials: "include",
    });
    if (res.ok) {
      const data = await res.json();
      setWatchdogStatus(data.status);
    }
  };
  // Notification Controls
  const [notifType, setNotifType] = useState("Urgent");
  const [notifFreq, setNotifFreq] = useState("Immediate");
  const [notifFormat, setNotifFormat] = useState("Voice");
  const [notifAuthority, setNotifAuthority] = useState("Needs Approval");
  const handleSendNotification = async () => {
    await fetch("/api/owner/notification", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({
        notification_type: notifType,
        message: `Test notification: ${notifType}`,
      }),
    });
    alert("Test notification sent!");
  };
  // Voice Demo (stub)
  const handleVoiceDemo = () => {
    alert(
      "Playing EMMA voice demo: “Hello, love. This is your Empress, always here for you.” (Australian, hyper-realistic, sultry)",
    );
  };
  // Biometric Auth
  const handleBiometric = async (type) => {
    const res = await fetch("/api/owner/biometric-auth", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ biometric_type: type }),
    });
    if (res.ok) setBiometricStatus(`${type} authenticated (static stub)`);
    else setBiometricStatus("Failed");
  };
  return (
    <div style={{ padding: 20 }}>
      <h3>Integrations, Security & EMMA</h3>
      {/* EmmaAvatar Mode Selection & Onboarding */}
      <div style={{ marginBottom: 24 }}>
        <div style={{ fontWeight: 600, marginBottom: 8 }}>Emma Avatar Mode</div>
        <div style={{ display: "flex", gap: 12 }}>
          <Button
            aria-label="Lifestyle Mode"
            variant="contained"
            color="primary"
            onClick={() =>
              onPrefsChange && onPrefsChange({ avatarMode: "lifestyle" })
            }
          >
            Lifestyle
          </Button>
          <Button
            aria-label="Naughty Mode"
            variant="outlined"
            color="secondary"
            onClick={() =>
              onPrefsChange && onPrefsChange({ avatarMode: "naughty" })
            }
          >
            Naughty
          </Button>
          <Button
            aria-label="Custom Mode"
            variant="outlined"
            color="default"
            onClick={() =>
              onPrefsChange && onPrefsChange({ avatarMode: "custom" })
            }
          >
            Custom
          </Button>
        </div>
        <Button
          aria-label="Avatar Onboarding"
          style={{ marginTop: 12 }}
          variant="outlined"
          color="primary"
          onClick={() =>
            alert("Starting Emma Avatar, PMP, and PLC onboarding tutorial...")
          }
        >
          Avatar & Muse Haven Tutorial
        </Button>
      </div>
      {/* Biometric Multi-Factor Authentication */}
      <div style={{ marginBottom: 24 }}>
        <div style={{ fontWeight: 600, marginBottom: 8 }}>
          Biometric Authentication
        </div>
        <div style={{ display: "flex", gap: 12 }}>
          <Button
            aria-label="Face Scan"
            variant="outlined"
            onClick={() => handleBiometric("face")}
          >
            Face
          </Button>
          <Button
            aria-label="Retina Scan"
            variant="outlined"
            onClick={() => handleBiometric("retina")}
          >
            Retina
          </Button>
          <Button
            aria-label="Fingerprint Scan"
            variant="outlined"
            onClick={() => handleBiometric("fingerprint")}
          >
            Fingerprint
          </Button>
          <Button
            aria-label="Voiceprint Scan"
            variant="outlined"
            onClick={() => handleBiometric("voice")}
          >
            Voice
          </Button>
        </div>
      </div>
      {/* Approval Mode */}
      <div style={{ marginBottom: 12 }}>
        <InputLabel id="approval-mode-label">Owner Approval Mode</InputLabel>
        <Select
          labelId="approval-mode-label"
          value={approvalMode}
          onChange={(e) => handleSetApprovalMode(e.target.value)}
          style={{ minWidth: 180 }}
        >
          {approvalModes.map((mode) => (
            <MenuItem key={mode.value} value={mode.value}>
              {mode.label}
            </MenuItem>
          ))}
        </Select>
      </div>
      {/* Notification Preferences */}
      <div style={{ marginBottom: 12 }}>
        <b>Notification Preferences:</b>
        <Tooltip title="Toggle Slack notifications for owner events.">
          <FormControlLabel
            control={
              <Switch
                checked={notificationPrefs.slack}
                onChange={(e) =>
                  onPrefsChange({
                    ...notificationPrefs,
                    slack: e.target.checked,
                  })
                }
              />
            }
            label="Slack"
          />
        </Tooltip>
        <Tooltip title="Toggle Discord notifications for owner events.">
          <FormControlLabel
            control={
              <Switch
                checked={notificationPrefs.discord}
                onChange={(e) =>
                  onPrefsChange({
                    ...notificationPrefs,
                    discord: e.target.checked,
                  })
                }
              />
            }
            label="Discord"
          />
        </Tooltip>
        <Tooltip title="Toggle Email notifications for owner events.">
          <FormControlLabel
            control={
              <Switch
                checked={notificationPrefs.email}
                onChange={(e) =>
                  onPrefsChange({
                    ...notificationPrefs,
                    email: e.target.checked,
                  })
                }
              />
            }
            label="Email"
          />
        </Tooltip>
      </div>
      {/* Notification Controls */}
      <div style={{ marginBottom: 12 }}>
        <InputLabel id="notif-type-label">Notification Type</InputLabel>
        <Select
          labelId="notif-type-label"
          value={notifType}
          onChange={(e) => setNotifType(e.target.value)}
          style={{ minWidth: 140 }}
        >
          {notificationTypes.map((type) => (
            <MenuItem key={type} value={type}>
              {type}
            </MenuItem>
          ))}
        </Select>
        <InputLabel id="notif-freq-label" style={{ marginLeft: 16 }}>
          Frequency
        </InputLabel>
        <Select
          labelId="notif-freq-label"
          value={notifFreq}
          onChange={(e) => setNotifFreq(e.target.value)}
          style={{ minWidth: 120 }}
        >
          {notificationFrequencies.map((freq) => (
            <MenuItem key={freq} value={freq}>
              {freq}
            </MenuItem>
          ))}
        </Select>
        <InputLabel id="notif-format-label" style={{ marginLeft: 16 }}>
          Format
        </InputLabel>
        <Select
          labelId="notif-format-label"
          value={notifFormat}
          onChange={(e) => setNotifFormat(e.target.value)}
          style={{ minWidth: 120 }}
        >
          {notificationFormats.map((fmt) => (
            <MenuItem key={fmt} value={fmt}>
              {fmt}
            </MenuItem>
          ))}
        </Select>
        <InputLabel id="notif-auth-label" style={{ marginLeft: 16 }}>
          Authority
        </InputLabel>
        <Select
          labelId="notif-auth-label"
          value={notifAuthority}
          onChange={(e) => setNotifAuthority(e.target.value)}
          style={{ minWidth: 160 }}
        >
          {authorityLevels.map((auth) => (
            <MenuItem key={auth} value={auth}>
              {auth}
            </MenuItem>
          ))}
        </Select>
        <Button
          variant="outlined"
          style={{ marginLeft: 16 }}
          onClick={handleSendNotification}
        >
          Send Test Notification
        </Button>
      </div>
      {/* API Key/Compliance */}
      <div style={{ marginTop: 20 }}>
        <Tooltip title="Rotate all API keys (owner only, static logic)">
          <Button variant="outlined" onClick={onRotateApiKey}>
            Rotate API Keys
          </Button>
        </Tooltip>
        <Tooltip title="Run static compliance audit and export log.">
          <Button
            variant="outlined"
            style={{ marginLeft: 10 }}
            onClick={onComplianceAudit}
          >
            Compliance Audit
          </Button>
        </Tooltip>
      </div>
      {/* Legal Sentinel */}
      <div
        style={{
          marginTop: 24,
          padding: 12,
          background: "#222",
          borderRadius: 8,
          color: "#fff",
        }}
      >
        <b>EMMA Legal Sentinel</b>
        <br />
        <span>Status: {emmaStatus ? "Active" : "Loading..."}</span>
        <br />
        <span>
          Domains: {emmaStatus ? emmaStatus.legal_domains.join(", ") : ""}
        </span>
        <br />
        <TextField
          label="Contract Text"
          multiline
          minRows={2}
          maxRows={6}
          value={contractText}
          onChange={(e) => setContractText(e.target.value)}
          style={{ width: "100%", marginTop: 8 }}
        />
        <Button
          variant="contained"
          style={{ marginTop: 8 }}
          onClick={handleLegalScan}
        >
          Scan Contract
        </Button>
        {contractReview && (
          <div style={{ marginTop: 8, color: "#4cafef" }}>{contractReview}</div>
        )}
      </div>
      {/* Anti-Sentience Watchdog */}
      <div
        style={{
          marginTop: 24,
          padding: 12,
          background: "#222",
          borderRadius: 8,
          color: "#fff",
        }}
      >
        <b>Anti-Sentience Watchdog</b>
        <br />
        <Button
          variant="contained"
          style={{ marginTop: 8 }}
          onClick={handleWatchdogScan}
        >
          Run Watchdog Scan
        </Button>
        {watchdogStatus && (
          <div style={{ marginTop: 8, color: "#4cafef" }}>{watchdogStatus}</div>
        )}
      </div>
      {/* Voice Demo */}
      <div style={{ marginTop: 24 }}>
        <Button
          variant="contained"
          color="secondary"
          onClick={handleVoiceDemo}
          aria-label="Play EMMA Voice Demo"
        >
          Hear EMMA's Voice
        </Button>
      </div>
    </div>
  );
}
