import React, { useEffect, useState } from 'react';
import Stats from './components/Stats';
import { EventTypePie, ErrorBar } from './components/EventCharts';
import Phase8ModulesDashboard from './Phase8ModulesDashboard';
import Phase9ModulesDashboard from './Phase9ModulesDashboard';

import Phase9AuditLogWidget from './components/Phase9AuditLogWidget';

function Phase9ApiStatus() {
  const [status, setStatus] = useState('Checking...');
  const [color, setColor] = useState('#aaa');
  const apiKey = localStorage.getItem('phase9_api_key') || 'PHASE9SAFEKEY';
  useEffect(() => {
    fetch('http://localhost:8090/phase9/global_trend_forecast', {
      headers: { 'Authorization': `Bearer ${apiKey}` }
    })
      .then(r => setStatus(r.ok ? 'Online' : 'Error'))
      .catch(() => setStatus('Offline'));
  }, [apiKey]);
  useEffect(() => {
    if (status === 'Online') setColor('#27b36a');
    else if (status === 'Error') setColor('#d67');
    else setColor('#aaa');
  }, [status]);
  return (
    <span style={{float:'right', fontWeight:500, color, fontSize:16, marginLeft:16}}>
      Phase 9+ API: {status}
    </span>
  );
}

function Phase9AuditLogPreview() {
  const [lines, setLines] = useState([]);
  useEffect(() => {
    fetch('/distribution/legal_exports/phase9_empire_audit_log.txt')
      .then(r => r.ok ? r.text() : '')
      .then(txt => setLines(txt.split('\n').filter(Boolean).slice(-5)));
  }, []);
  return (
    <div style={{background:'#f8f8fa', border:'1px solid #eee', borderRadius:6, padding:8, margin:'18px 0 10px 0', width:400}}>
      <b style={{fontSize:14}}>Phase 9+ Audit Log (Recent)</b>
      <pre style={{fontSize:12, margin:0, background:'none', padding:0}}>{lines.length ? lines.join('\n') : 'No entries.'}</pre>
    </div>
  );
}

function App() {
  const [events, setEvents] = useState([]);
  const [logType, setLogType] = useState('fulfillment_log.json');

  useEffect(() => {
    fetch(`/api/events/${logType}`)
      .then(res => res.json())
      .then(setEvents);
  }, [logType]);

  const [view, setView] = useState('main');
  return (
    <div style={{padding: 20}}>
      <h1>AIFOLIO Event Dashboard <Phase9ApiStatus /></h1>
      <div style={{marginBottom: 16}}>
        <button onClick={() => setView('main')} style={{marginRight: 12}}>Event Dashboard</button>
        <button onClick={() => setView('phase8')} style={{marginRight: 12}}>SAFE AI Phase 8 Modules</button>
        <button onClick={() => setView('phase9')}>SAFE AI Phase 9+ Empire Modules</button>
      </div>
      {view === 'main' && <Phase9AuditLogPreview />}

      {view === 'main' && (
        <>
          <select value={logType} onChange={e => setLogType(e.target.value)}>
            <option value="fulfillment_log.json">Fulfillment</option>
            <option value="refund_log.json">Refund</option>
            <option value="vault_activity_log.json">Vault Activity</option>
            <option value="delivery_log.json">Delivery</option>
            <option value="error_log.json">Errors</option>
            <option value="metadata_update_log.json">Metadata Update</option>
            <option value="vault_sales_log.json">Sales</option>
          </select>
          <Stats events={events} />
          <div style={{display:'flex', gap:40, marginBottom:32}}>
            <div style={{width:320}}>
              <h3>Event Type Distribution</h3>
              <EventTypePie events={events} />
            </div>
            <div style={{width:480}}>
              <h3>Errors by Event Type</h3>
              <ErrorBar events={events} />
            </div>
          </div>
          <table border="1" cellPadding="8" style={{marginTop: 20, width: '100%'}}>
            <thead>
              <tr>
                <th>#</th>
                <th>Timestamp</th>
                <th>Type</th>
                <th>Details</th>
              </tr>
            </thead>
            <tbody>
              {events.map((event, i) => (
                <tr key={i}>
                  <td>{i + 1}</td>
                  <td>{event.timestamp}</td>
                  <td>{event.type}</td>
                  <td>{event.details}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </>
      )}
      {view === 'phase8' && (
        <Phase8ModulesDashboard />
      )}
      {view === 'phase9' && (
        <Phase9ModulesDashboard />
      )}

                <th>#</th>
                <th>Timestamp</th>
                <th>Event</th>
                <th>Vault ID</th>
                <th>Details</th>
              </tr>
            </thead>
            <tbody>
              {events.map((ev, i) => (
                <tr key={i}>
                  <td>{i+1}</td>
                  <td>{ev.timestamp}</td>
                  <td>{ev.event}</td>
                  <td>{ev.vault_id || ev.run_id || ''}</td>
                  <td><pre style={{maxWidth: 400, whiteSpace: 'pre-wrap'}}>{JSON.stringify(ev, null, 2)}</pre></td>
                </tr>
              ))}
            </tbody>
          </table>
        </>
      )}
      {view === 'phase8' && <Phase8ModulesDashboard />}
    </div>
  );
}

export default App;
