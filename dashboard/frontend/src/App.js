import React, { useEffect, useState } from 'react';
import Stats from './components/Stats';
import { EventTypePie, ErrorBar } from './components/EventCharts';
import Phase8ModulesDashboard from './Phase8ModulesDashboard';

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
      <h1>AIFOLIO Event Dashboard</h1>
      <div style={{marginBottom: 16}}>
        <button onClick={() => setView('main')} style={{marginRight: 12}}>Event Dashboard</button>
        <button onClick={() => setView('phase8')}>SAFE AI Phase 8 Modules</button>
      </div>
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
