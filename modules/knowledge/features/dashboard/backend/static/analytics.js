// Interactive Analytics Dashboard for AIFOLIO™
// Uses Chart.js for charts and heatmaps
// Assumes analytics, compliance, and risk data available via /api endpoints

let chartInstances = {};

function fetchAndRender(endpoint, renderFn) {
  fetch(endpoint)
    .then((res) => res.json())
    .then((data) => renderFn(data));
}

function renderTrends(data) {
  const ctx = document.getElementById("trendChart").getContext("2d");
  if (chartInstances.trend) chartInstances.trend.destroy();
  chartInstances.trend = new Chart(ctx, {
    type: "line",
    data: {
      labels: data.labels,
      datasets: [
        {
          label: "Compliance Events",
          data: data.values,
          backgroundColor: "rgba(176, 211, 106, 0.2)",
          borderColor: "#b0d36a",
          borderWidth: 2,
          fill: true,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false } },
    },
  });
}

function renderRiskHeatmap(data) {
  // Display compliance alerts if present
  const alertDiv = document.getElementById("complianceAlerts");
  if (data.alerts && data.alerts.length > 0) {
    alertDiv.innerHTML = data.alerts.map((a) => `<div>${a}</div>`).join("");
  } else {
    alertDiv.innerHTML = "";
  }
  const ctx = document.getElementById("riskHeatmap").getContext("2d");
  if (chartInstances.heatmap) chartInstances.heatmap.destroy();
  chartInstances.heatmap = new Chart(ctx, {
    type: "matrix",
    data: {
      datasets: [
        {
          label: "Compliance Risk",
          data: data.cells,
          backgroundColor: (ctx) => {
            const v = ctx.dataset.data[ctx.dataIndex].v;
            return v > 7 ? "#e74c3c" : v > 4 ? "#ffd900" : "#b0d36a";
          },
          width: ({ chart }) => (chart.chartArea || {}).width / data.cols - 2,
          height: ({ chart }) => (chart.chartArea || {}).height / data.rows - 2,
        },
      ],
    },
    options: {
      plugins: { legend: { display: false } },
      scales: {
        x: { type: "category", labels: data.xLabels },
        y: { type: "category", labels: data.yLabels },
      },
    },
  });
}

function renderReviewerStats(stats, escalations) {
  // Chart: reviewer event counts
  const ctx = document.getElementById("reviewerStatsChart").getContext("2d");
  if (chartInstances.reviewer) chartInstances.reviewer.destroy();
  chartInstances.reviewer = new Chart(ctx, {
    type: "bar",
    data: {
      labels: stats.map((s) => s.reviewer),
      datasets: [
        {
          label: "Events",
          data: stats.map((s) => s.events),
          backgroundColor: "#b0d36a",
        },
      ],
    },
    options: { responsive: true, plugins: { legend: { display: false } } },
  });
  // Table
  const tbody = document.querySelector("#reviewerStatsTable tbody");
  tbody.innerHTML = stats
    .map(
      (s) =>
        `<tr>
            <td>${s.reviewer}</td>
            <td>${s.events}</td>
            <td>${s.last_activity}</td>
            <td>${s.avg_response_time}</td>
            <td>${s.accuracy_rate}</td>
            <td>${s.total_reviews}</td>
            <td>${s.escalation_rate}</td>
            <td>${s.escalations}</td>
            <td><button class='escalate-btn' data-rev='${s.reviewer}'>Escalate</button></td>
        </tr>`,
    )
    .join("");
  document.querySelectorAll(".escalate-btn").forEach((btn) => {
    btn.onclick = function () {
      document.getElementById("escalateReviewer").value = btn.dataset.rev;
      document.getElementById("escalationForm").style.display = "";
    };
  });
  // Escalation List
  const escDiv = document.getElementById("escalationList");
  if (escDiv) {
    escDiv.innerHTML =
      "<h4>Escalation Workflow</h4>" +
      (escalations.length
        ? '<table style="width:100%;border-collapse:collapse;"><thead><tr><th>Reviewer</th><th>Reason</th><th>Timestamp</th><th>State</th><th>Resolution</th><th>Action</th></tr></thead><tbody>' +
          escalations
            .map(
              (e) =>
                `<tr>
                <td>${e.reviewer}</td>
                <td>${e.reason}</td>
                <td>${e.timestamp}</td>
                <td>${e.state}</td>
                <td>${e.resolution_reason || ""}</td>
                <td>${e.state === "pending" ? `<button class='resolve-escalation' data-rev='${e.reviewer}' data-ts='${e.timestamp}' data-action='resolved'>Resolve</button> <button class='reject-escalation' data-rev='${e.reviewer}' data-ts='${e.timestamp}' data-action='rejected'>Reject</button>` : ""}</td>
            </tr>`,
            )
            .join("") +
          "</tbody></table>"
        : '<div style="color:#e74c3c;">No escalations.</div>');
    escDiv
      .querySelectorAll(".resolve-escalation,.reject-escalation")
      .forEach((btn) => {
        btn.onclick = function () {
          const reviewer = btn.dataset.rev;
          const timestamp = btn.dataset.ts;
          const state = btn.dataset.action;
          const reason = prompt("Enter resolution reason:") || "";
          fetch("/api/analytics/reviewer_escalations", {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              reviewer,
              timestamp,
              state,
              resolution_reason: reason,
            }),
          })
            .then((r) => r.json())
            .then(() => fetchReviewerAnalytics());
        };
      });
  }
}

document.addEventListener("DOMContentLoaded", function () {
  fetchAndRender("/api/analytics/trends", renderTrends);
  fetchAndRender("/api/analytics/risk_heatmap", renderRiskHeatmap);

  // Theme switcher
  const themeSelect = document.getElementById("themeSelect");
  function setTheme(theme) {
    document.body.className = theme;
    localStorage.setItem("aifolio_theme", theme);
  }
  if (themeSelect) {
    themeSelect.value = localStorage.getItem("aifolio_theme") || "dark";
    setTheme(themeSelect.value);
    themeSelect.addEventListener("change", function () {
      setTheme(this.value);
    });
  } else {
    setTheme(localStorage.getItem("aifolio_theme") || "dark");
  }

  // Notification Settings
  const notifForm = document.getElementById("notificationSettingsForm");
  const notifInApp = document.getElementById("notifInApp");
  const notifEmail = document.getElementById("notifEmail");
  const notifSaved = document.getElementById("notifSettingsSaved");
  // Load from backend
  fetch("/api/notification_settings")
    .then((r) => r.json())
    .then((settings) => {
      notifInApp.checked = settings.in_app !== false;
      notifEmail.checked = settings.email === true;
    });
  notifForm.onsubmit = function (e) {
    e.preventDefault();
    fetch("/api/notification_settings", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        in_app: notifInApp.checked,
        email: notifEmail.checked,
      }),
    }).then((r) => (r.ok ? (notifSaved.style.display = "inline") : null));
    setTimeout(() => {
      notifSaved.style.display = "none";
    }, 1500);
  };

  // Advanced Audit Search
  const auditForm = document.getElementById("auditSearchForm");
  const auditLoading = document.getElementById("auditLoading");
  const auditEmpty = document.getElementById("auditEmptyState");
  auditForm.onsubmit = function (e) {
    e.preventDefault();
    const q = document.getElementById("auditQuery").value;
    const dateFrom = document.getElementById("auditDateFrom").value;
    const dateTo = document.getElementById("auditDateTo").value;
    const actionType = document.getElementById("auditActionType").value;
    auditLoading.style.display = "block";
    auditEmpty.style.display = "none";
    fetch(
      `/api/audit/search?q=${encodeURIComponent(q)}&date_from=${encodeURIComponent(dateFrom)}&date_to=${encodeURIComponent(dateTo)}&action_type=${encodeURIComponent(actionType)}`,
    )
      .then((r) => r.json())
      .then((res) => {
        const table = document.getElementById("auditResultsTable");
        const tbody = table.querySelector("tbody");
        auditLoading.style.display = "none";
        if (res.results && res.results.length) {
          tbody.innerHTML = res.results
            .map(
              (row) =>
                `<tr><td>${row.timestamp}</td><td>${row.user}</td><td>${row.action}</td><td>${row.ip}</td></tr>`,
            )
            .join("");
          table.style.display = "";
          auditEmpty.style.display = "none";
        } else {
          tbody.innerHTML = "";
          table.style.display = "none";
          auditEmpty.style.display = "";
        }
      });
  };

  // In-app notifications for compliance alerts
  function pollNotifications() {
    fetch("/api/notifications")
      .then((r) => r.json())
      .then((data) => {
        const notifDiv = document.getElementById("inAppNotifications");
        if (notifDiv && data.alerts && data.alerts.length) {
          notifDiv.innerHTML = data.alerts
            .map((a) => `<div class='alert'>${a}</div>`)
            .join("");
        }
      });
    setTimeout(pollNotifications, 15000);
  }
  pollNotifications();

  // AJAX for custom legal template upload/edit
  const customForm = document.getElementById("customLegalForm");
  if (customForm) {
    customForm.addEventListener("submit", function (e) {
      e.preventDefault();
      const statusDiv = document.getElementById("customLegalStatus");
      statusDiv.textContent = "Uploading...";
      const formData = new FormData(customForm);
      fetch("/legal_export/custom", {
        method: "POST",
        body: formData,
      })
        .then((resp) => {
          if (resp.ok) return resp.blob();
          return resp.text().then((t) => {
            throw new Error(t);
          });
        })
        .then((blob) => {
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement("a");
          a.href = url;
          a.download = "AIFOLIO_CustomLegal.txt";
          a.textContent = "Download Custom Legal Template";
          statusDiv.innerHTML = "";
          statusDiv.appendChild(a);
          loadCustomTemplates();
        })
        .catch((err) => {
          statusDiv.textContent = "Error: " + err.message;
        });
    });
  }

  // List/download/delete custom legal templates
  function loadCustomTemplates() {
    fetch("/legal_export/custom/list")
      .then((r) => r.json())
      .then((list) => {
        const listDiv = document.getElementById("customLegalList");
        if (!listDiv) return;
        listDiv.innerHTML = list
          .map(
            (t) => `
                <div class='template-item'>
                    <a href="/legal_export/custom/download/${t.filename}" target="_blank">${t.filename}</a>
                    <span>(${t.created})</span>
                    <button data-fn="${t.filename}" class="delete-template">Delete</button>
                </div>
            `,
          )
          .join("");
        listDiv.querySelectorAll(".delete-template").forEach((btn) => {
          btn.onclick = function () {
            fetch("/legal_export/custom/delete/" + btn.dataset.fn, {
              method: "POST",
            }).then((r) => {
              if (r.ok) loadCustomTemplates();
            });
          };
        });
      });
  }
  loadCustomTemplates();
});
