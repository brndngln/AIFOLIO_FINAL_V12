// compliance_dashboard.js
// Real-time admin alerts, risk visuals, audit log, and regulatory API integration

document.addEventListener('DOMContentLoaded', () => {
    fetchAuditLog();
    fetchAlerts();
    fetchRegApiStatus();
    fetchComplianceCharts();
    renderRiskMeter(0.2); // Placeholder risk
    renderComplianceSummary();
    fetchUserActivity();
    fetchAnomalyTimeline();
    fetchRegulatoryNews();
    fetchGeolocationAnalytics();
    fetchDeviceRisk();
    fetchCustomAnomalyDetection();
    fetchExternalComplianceFeeds();
    fetchAdvancedReporting();
});

function fetchAuditLog() {
    fetch('/api/audit-log')
        .then(res => res.json())
        .then(data => {
            const tbody = document.querySelector('#auditTable tbody');
            tbody.innerHTML = '';
            data.forEach(entry => {
                const row = document.createElement('tr');
                row.innerHTML = `<td>${entry.time}</td><td>${entry.event}</td><td>${entry.user}</td><td>${entry.details}</td>`;
                tbody.appendChild(row);
            });
        });
}

function fetchAlerts() {
    fetch('/api/alerts')
        .then(res => res.json())
        .then(data => {
            const feed = document.getElementById('alert-feed');
            feed.innerHTML = '';
            data.forEach(alert => {
                const div = document.createElement('div');
                div.className = 'alert';
                div.textContent = `[${alert.level}] ${alert.message}`;
                feed.appendChild(div);
            });
        });
}

function fetchRegApiStatus() {
    fetch('/api/regulatory-status')
        .then(res => res.json())
        .then(data => {
            document.getElementById('regApiStatus').textContent = data.status;
        });
}

function renderRiskMeter(risk) {
    // Simple risk meter (0-1 scale)
    const ctx = document.getElementById('riskMeter').getContext('2d');
    ctx.clearRect(0, 0, 400, 200);
    ctx.fillStyle = risk > 0.7 ? 'red' : risk > 0.4 ? 'orange' : 'green';
    ctx.fillRect(50, 100, 300 * risk, 50);
    ctx.strokeRect(50, 100, 300, 50);
    ctx.font = '16px Arial';
    ctx.fillStyle = '#222';
    ctx.fillText(`Risk Level: ${(risk * 100).toFixed(1)}%`, 160, 130);
}

function fetchComplianceCharts() {
    fetch('/api/compliance-charts')
        .then(res => res.json())
        .then(data => {
            renderEventBreakdownPieChart(data.eventBreakdown);
            renderRiskOverTimeLineChart(data.riskOverTime);
            renderEventBreakdownChart(data.eventBreakdown); // Keep bar chart for drilldown
            renderHeatmapWidget();
        });
    fetchComplianceChecks();
    fetchRegulatoryAPIStatus();
}

function renderEventBreakdownPieChart(eventBreakdown) {
    let container = document.getElementById('eventBreakdownPie');
    if (!container) {
        container = document.createElement('div');
        container.id = 'eventBreakdownPie';
        document.getElementById('risk-visuals').appendChild(container);
    }
    container.innerHTML = '<h3>Event Breakdown (Pie)</h3><canvas id="pieChart" width="300" height="200"></canvas>';
    const ctx = document.getElementById('pieChart').getContext('2d');
    if (window.pieChartObj) window.pieChartObj.destroy();
    window.pieChartObj = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: Object.keys(eventBreakdown),
            datasets: [{
                data: Object.values(eventBreakdown),
                backgroundColor: ['#3af','#f80','#0c0','#f33','#09c','#fa0','#c3f'],
            }]
        },
        options: {responsive: false, plugins: {legend: {display: true}}}
    });
}

function renderEventBreakdownChart(eventBreakdown) {
    let container = document.getElementById('eventBreakdownChart');
    if (!container) {
        container = document.createElement('div');
        container.id = 'eventBreakdownChart';
        document.getElementById('risk-visuals').appendChild(container);
    }
    container.innerHTML = '<h3>Event Breakdown</h3>';
    const total = Object.values(eventBreakdown).reduce((a, b) => a + b, 0);
    Object.entries(eventBreakdown).forEach(([event, count]) => {
        const bar = document.createElement('div');
        bar.className = 'event-bar';
        bar.style.width = `${Math.max(10, (count / total) * 300)}px`;
        bar.style.background = '#3af';
        bar.style.margin = '4px 0';
        bar.style.cursor = 'pointer';
        bar.textContent = `${event}: ${count}`;
        bar.onclick = () => showEventDrilldown(event);
        container.appendChild(bar);
    });
}

function renderRiskOverTimeLineChart(riskOverTime) {
    let container = document.getElementById('riskOverTimeLine');
    if (!container) {
        container = document.createElement('div');
        container.id = 'riskOverTimeLine';
        document.getElementById('risk-visuals').appendChild(container);
    }
    container.innerHTML = '<h3>Risk Over Time (Line)</h3><canvas id="riskLineChart" width="400" height="120"></canvas>';
    const ctx = document.getElementById('riskLineChart').getContext('2d');
    if (window.riskLineChartObj) window.riskLineChartObj.destroy();
    window.riskLineChartObj = new Chart(ctx, {
        type: 'line',
        data: {
            labels: riskOverTime.map((_,i)=>i+1),
            datasets: [{label:'Risk',data:riskOverTime.map(pt=>pt.y),fill:false,borderColor:'#f80',tension:0.2}]
        },
        options: {responsive: false, plugins: {legend: {display: false}}}
    });
}

function renderHeatmapWidget() {
    let container = document.getElementById('auditHeatmap');
    if (!container) {
        container = document.createElement('div');
        container.id = 'auditHeatmap';
        document.getElementById('risk-visuals').appendChild(container);
    }
    container.innerHTML = '<h3>Audit Event Heatmap (Simulated)</h3><canvas id="heatmapCanvas" width="400" height="120"></canvas>';
    const ctx = document.getElementById('heatmapCanvas').getContext('2d');
    // Simulate heatmap data
    for (let x=0; x<20; x++) {
        for (let y=0; y<6; y++) {
            const val = Math.random();
            ctx.fillStyle = `rgba(255,80,0,${val*0.7+0.2})`;
            ctx.fillRect(20*x, 20*y, 18, 18);
        }
    }
}


function renderRiskOverTimeChart(riskOverTime) {
    let container = document.getElementById('riskOverTimeChart');
    if (!container) {
        container = document.createElement('div');
        container.id = 'riskOverTimeChart';
        document.getElementById('risk-visuals').appendChild(container);
    }
    container.innerHTML = '<h3>Risk Over Time</h3>';
    const canvas = document.createElement('canvas');
    canvas.width = 400;
    canvas.height = 120;
    container.appendChild(canvas);
    const ctx = canvas.getContext('2d');
    ctx.strokeStyle = '#f80';
    ctx.beginPath();
    riskOverTime.forEach((pt, i) => {
        const x = 10 + (380 * i / (riskOverTime.length - 1));
        const y = 110 - (pt.y * 100);
        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
    });
    ctx.stroke();
}

function showEventDrilldown(eventType) {
    fetch('/api/audit-log')
        .then(res => res.json())
        .then(entries => {
            const details = entries.filter(e => e.event === eventType);
            let modal = document.getElementById('eventDrilldownModal');
            if (!modal) {
                modal = document.createElement('div');
                modal.id = 'eventDrilldownModal';
                modal.style.position = 'fixed';
                modal.style.top = '10%';
                modal.style.left = '50%';
                modal.style.transform = 'translateX(-50%)';
                modal.style.background = '#fff';
                modal.style.border = '1px solid #333';
                modal.style.padding = '20px';
                modal.style.zIndex = '1000';
                modal.style.maxHeight = '70vh';
                modal.style.overflowY = 'auto';
                document.body.appendChild(modal);
            }
            modal.innerHTML = `<h3>Drilldown: ${eventType}</h3>` +
                details.map(d => `<div style='border-bottom:1px solid #eee;padding:4px 0;'><b>${d.time}</b> [${d.user}]<br>${d.details}</div>`).join('') +
                '<button onclick="document.getElementById(\'eventDrilldownModal\').remove()">Close</button>';
        });
}

function renderComplianceSummary() {
    let container = document.getElementById('complianceSummary');
    if (!container) {
        container = document.createElement('section');
        container.id = 'complianceSummary';
        container.innerHTML = '<h2>Compliance Summary</h2><div id="summaryContent"></div>';
        document.querySelector('main').insertBefore(container, document.getElementById('alerts'));
    }
    fetch('/api/compliance-charts')
        .then(res => res.json())
        .then(data => {
            const totalEvents = Object.values(data.eventBreakdown).reduce((a,b) => a+b, 0);
            document.getElementById('summaryContent').innerHTML =
                `<b>Total Audit Events:</b> ${totalEvents}<br>` +
                Object.entries(data.eventBreakdown).map(([k,v])=>`${k}: <b>${v}</b>`).join(' | ');
        });
    renderComplianceCheckWidget();
    renderRegulatoryAPIWidget();
    renderUserActivityWidget();
    renderAnomalyTimelineWidget();
    renderRegulatoryNewsWidget();
    renderGeolocationAnalyticsWidget();
    renderDeviceRiskWidget();
    renderCustomAnomalyDetectionWidget();
    renderExternalComplianceFeedsWidget();
    renderAdvancedReportingWidget();
}

function fetchComplianceChecks() {
    fetch('/api/compliance-checks')
        .then(res => res.json())
        .then(data => renderComplianceCheckWidget(data.checks));
}

function renderComplianceCheckWidget(checks) {
    let container = document.getElementById('complianceCheckWidget');
    if (!container) {
        container = document.createElement('div');
        container.id = 'complianceCheckWidget';
        document.getElementById('complianceSummary').appendChild(container);
    }
    if (!checks) return;
    container.innerHTML = '<h3>Automated Compliance Checks</h3><canvas id="complianceBar" width="350" height="120"></canvas>';
    const ctx = document.getElementById('complianceBar').getContext('2d');
    if (window.complianceBarObj) window.complianceBarObj.destroy();
    window.complianceBarObj = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: checks.map(c=>c.check),
            datasets: [{label:'Status',data:checks.map(c=>c.status==='PASS'?1:0),backgroundColor:checks.map(c=>c.status==='PASS'?'#0c0':'#f33')}]
        },
        options: {responsive: false, plugins: {legend: {display: false}},scales:{y:{min:0,max:1,ticks:{callback:v=>v?'PASS':'FAIL'}}}}
    });
}

function fetchUserActivity() {
    fetch('/api/user-activity')
        .then(res => res.json())
        .then(data => renderUserActivityWidget(data.activity));
}

function renderUserActivityWidget(activity) {
    let container = document.getElementById('userActivityWidget');
    if (!container) {
        container = document.createElement('div');
        container.id = 'userActivityWidget';
        document.getElementById('complianceSummary').appendChild(container);
    }
    if (!activity) return;
    container.innerHTML = '<h3>User Activity</h3>' +
        `<table style='width:100%;border-collapse:collapse;'><tr><th>User</th><th>Actions</th><th>Last Active</th><th>IP</th><th>Device</th></tr>` +
        activity.map(u=>`<tr><td>${u.user}</td><td>${u.actions}</td><td>${u.last_active}</td><td>${u.ip||''}</td><td>${u.device||''}</td></tr>`).join('') + '</table>';
}

function fetchAnomalyTimeline() {
    fetch('/api/anomaly-timeline')
        .then(res => res.json())
        .then(data => renderAnomalyTimelineWidget(data.timeline));
}

function renderAnomalyTimelineWidget(timeline) {
    let container = document.getElementById('anomalyTimelineWidget');
    if (!container) {
        container = document.createElement('div');
        container.id = 'anomalyTimelineWidget';
        document.getElementById('complianceSummary').appendChild(container);
    }
    if (!timeline) return;
    container.innerHTML = '<h3>Anomaly Timeline</h3><canvas id="anomalyLine" width="350" height="120"></canvas>';
    const ctx = document.getElementById('anomalyLine').getContext('2d');
    if (window.anomalyLineObj) window.anomalyLineObj.destroy();
    window.anomalyLineObj = new Chart(ctx, {
        type: 'line',
        data: {
            labels: timeline.map(t=>t.time.split('T')[1]),
            datasets: [{label:'Anomalies',data:timeline.map(t=>t.anomalies),fill:false,borderColor:'#f33',tension:0.2}]
        },
        options: {responsive: false, plugins: {legend: {display: false}}}
    });
}

function fetchGeolocationAnalytics() {
    fetch('/api/geolocation-analytics')
        .then(res => res.json())
        .then(data => renderGeolocationAnalyticsWidget(data.geo));
}

function renderGeolocationAnalyticsWidget(geo) {
    let container = document.getElementById('geolocationAnalyticsWidget');
    if (!container) {
        container = document.createElement('div');
        container.id = 'geolocationAnalyticsWidget';
        document.getElementById('complianceSummary').appendChild(container);
    }
    if (!geo) return;
    container.innerHTML = '<h3>Geolocation Analytics</h3><canvas id="geoBar" width="350" height="120"></canvas>';
    const ctx = document.getElementById('geoBar').getContext('2d');
    if (window.geoBarObj) window.geoBarObj.destroy();
    window.geoBarObj = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: geo.map(g=>g.country),
            datasets: [{label:'Events',data:geo.map(g=>g.events),backgroundColor:'#3af'}]
        },
        options: {responsive: false, plugins: {legend: {display: false}}}
    });
}

function fetchDeviceRisk() {
    fetch('/api/device-risk')
        .then(res => res.json())
        .then(data => renderDeviceRiskWidget(data.devices));
}

function renderDeviceRiskWidget(devices) {
    let container = document.getElementById('deviceRiskWidget');
    if (!container) {
        container = document.createElement('div');
        container.id = 'deviceRiskWidget';
        document.getElementById('complianceSummary').appendChild(container);
    }
    if (!devices) return;
    container.innerHTML = '<h3>Device Risk</h3><canvas id="deviceRiskBar" width="350" height="120"></canvas>';
    const ctx = document.getElementById('deviceRiskBar').getContext('2d');
    if (window.deviceRiskBarObj) window.deviceRiskBarObj.destroy();
    window.deviceRiskBarObj = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: devices.map(d=>`${d.user} (${d.device})`),
            datasets: [{label:'Risk',data:devices.map(d=>d.risk),backgroundColor:devices.map(d=>d.risk>0.5?'#f33':'#0c0')}]
        },
        options: {responsive: false, plugins: {legend: {display: false}},scales:{y:{min:0,max:1,ticks:{callback:v=>(v*100).toFixed(0)+'%'}}}}
    });
}

function fetchCustomAnomalyDetection() {
    fetch('/api/custom-anomaly-detection')
        .then(res => res.json())
        .then(data => renderCustomAnomalyDetectionWidget(data.anomalies));
}

function renderCustomAnomalyDetectionWidget(anomalies) {
    let container = document.getElementById('customAnomalyDetectionWidget');
    if (!container) {
        container = document.createElement('div');
        container.id = 'customAnomalyDetectionWidget';
        document.getElementById('complianceSummary').appendChild(container);
    }
    if (!anomalies) return;
    container.innerHTML = '<h3>Custom Anomaly Detection</h3>' +
        anomalies.map(a=>`<div style='border-bottom:1px solid #eee;padding:4px 0;'><b>${a.type}</b> [${a.user}] <span style='color:${a.severity==='high'?'#f33':a.severity==='medium'?'#fa0':'#0c0'}'>${a.severity.toUpperCase()}</span> <span style='float:right'>${a.time}</span></div>`).join('');
}

function fetchExternalComplianceFeeds() {
    fetch('/api/external-compliance-feeds')
        .then(res => res.json())
        .then(data => renderExternalComplianceFeedsWidget(data.feeds));
}

function renderExternalComplianceFeedsWidget(feeds) {
    let container = document.getElementById('externalComplianceFeedsWidget');
    if (!container) {
        container = document.createElement('div');
        container.id = 'externalComplianceFeedsWidget';
        document.getElementById('complianceSummary').appendChild(container);
    }
    if (!feeds) return;
    container.innerHTML = '<h3>External Compliance Feeds</h3><ul>' +
        feeds.map(f=>`<li><a href="${f.url}" target="_blank" rel="noopener">${f.feed}</a></li>`).join('') + '</ul>';
}

function fetchAdvancedReporting() {
    fetch('/api/advanced-reporting')
        .then(res => res.json())
        .then(data => renderAdvancedReportingWidget(data));
}

function renderAdvancedReportingWidget(data) {
    let container = document.getElementById('advancedReportingWidget');
    if (!container) {
        container = document.createElement('div');
        container.id = 'advancedReportingWidget';
        document.getElementById('complianceSummary').appendChild(container);
    }
    if (!data) return;
    container.innerHTML = '<h3>Advanced Reporting</h3>' +
        `<b>Summary:</b> Events: ${data.summary.total_events}, Users: ${data.summary.unique_users}, Countries: ${data.summary.countries}<br>` +
        `<b>Trends:</b> ` + data.trends.map(t=>`${t.date}: ${t.events} events`).join(' | ') + '<br>' +
        `<b>Outliers:</b><ul>` + data.outliers.map(o=>`<li>${o.type} [${o.user}] at ${o.time}</li>`).join('') + '</ul>';
}

function fetchRegulatoryNews() {
    fetch('/api/regulatory-news')
        .then(res => res.json())
        .then(data => renderRegulatoryNewsWidget(data.news));
}

function renderRegulatoryNewsWidget(news) {
    let container = document.getElementById('regulatoryNewsWidget');
    if (!container) {
        container = document.createElement('div');
        container.id = 'regulatoryNewsWidget';
        document.getElementById('complianceSummary').appendChild(container);
    }
    if (!news) return;
    container.innerHTML = '<h3>Regulatory News</h3><ul>' +
        news.map(n=>`<li><a href="${n.url}" target="_blank" rel="noopener">${n.headline}</a></li>`).join('') + '</ul>';
}

function fetchRegulatoryAPIStatus() {
    fetch('/api/regulatory-api-status')
        .then(res => res.json())
        .then(data => renderRegulatoryAPIWidget(data));
}

function renderRegulatoryAPIWidget(data) {
    let container = document.getElementById('regulatoryAPIWidget');
    if (!container) {
        container = document.createElement('div');
        container.id = 'regulatoryAPIWidget';
        document.getElementById('complianceSummary').appendChild(container);
    }
    if (!data) {
        container.innerHTML = '<h3>Regulatory API Status</h3><span>Loading...</span>';
        return;
    }
    container.innerHTML = `<h3>Regulatory API Status</h3><b>Status:</b> ${data.status} <br><b>Source:</b> ${data.source||'N/A'} <br><b>Checked At:</b> ${data.checked_at||''}`;
}
