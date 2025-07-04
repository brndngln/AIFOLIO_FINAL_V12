import React, { useEffect, useState, useRef } from 'react';
import axios from 'axios';
import { Tooltip, Select, MenuItem, InputLabel, FormControl, TextField, Alert } from '@mui/material';

const getColor = (status) => {
  if (status === 'SUCCESS') return '#4CAF50';
  if (status === 'VERIFY_FAIL') return '#FFC107';
  if (status === 'FAIL' || status === 'FALLBACK_LAST_KNOWN') return '#F44336';
  return '#BDBDBD';
};

const unique = (arr, key) => Array.from(new Set(arr.map(x => x[key])));

const SecretRotationHeatmap = () => {
  const [data, setData] = useState([]);
  const [keyFilter, setKeyFilter] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [start, setStart] = useState('');
  const [end, setEnd] = useState('');
  const [error, setError] = useState('');
  const [alert, setAlert] = useState(null);
  const intervalRef = useRef(null);

  const fetchData = () => {
    let params = {};
    if (keyFilter) params.key = keyFilter;
    if (statusFilter) params.status = statusFilter;
    if (start) params.start = start;
    if (end) params.end = end;
    axios.get('/api/logs/secret_rotation', { params })
      .then(res => {
        setData(res.data);
        // Alert if any recent failure
        const last = res.data.slice(-1)[0];
        if (last && last.status !== 'SUCCESS') {
          setAlert(`ALERT: Last rotation failed at ${last.timestamp} (${last.key}: ${last.status})`);
        } else {
          setAlert(null);
        }
      })
      .catch(() => {
        setData([]);
        setError('Failed to load rotation data.');
      });
  };

  useEffect(() => {
    fetchData();
    intervalRef.current = setInterval(fetchData, 10000); // live refresh every 10s
    return () => clearInterval(intervalRef.current);
     
  }, [keyFilter, statusFilter, start, end]);

  // Group by day
  const byDay = {};
  data.forEach(entry => {
    const day = entry.timestamp.slice(0, 10);
    if (!byDay[day]) byDay[day] = [];
    byDay[day].push(entry);
  });
  const days = Object.keys(byDay).sort().slice(-30);

  // Stats
  const total = data.length;
  const failures = data.filter(e => e.status !== 'SUCCESS').length;
  const lastFail = data.filter(e => e.status !== 'SUCCESS').slice(-1)[0];
  const allKeys = unique(data, 'key');
  const allStatuses = unique(data, 'status');

  return (
    <div style={{padding: 16}}>
      <h3>Secret Rotation Heatmap (Last 30 Days)</h3>
      {alert && <Alert severity="error" style={{marginBottom:8}}>{alert}</Alert>}
      {error && <Alert severity="error">{error}</Alert>}
      <div style={{display:'flex',gap:12,marginBottom:12}}>
        <FormControl size="small">
          <InputLabel>Key</InputLabel>
          <Select value={keyFilter} label="Key" onChange={e=>setKeyFilter(e.target.value)} style={{minWidth:120}}>
            <MenuItem value="">All</MenuItem>
            {allKeys.map(k=>(<MenuItem value={k} key={k}>{k}</MenuItem>))}
          </Select>
        </FormControl>
        <FormControl size="small">
          <InputLabel>Status</InputLabel>
          <Select value={statusFilter} label="Status" onChange={e=>setStatusFilter(e.target.value)} style={{minWidth:120}}>
            <MenuItem value="">All</MenuItem>
            {allStatuses.map(s=>(<MenuItem value={s} key={s}>{s}</MenuItem>))}
          </Select>
        </FormControl>
        <TextField size="small" label="Start Date" type="date" value={start} onChange={e=>setStart(e.target.value)} InputLabelProps={{shrink:true}}/>
        <TextField size="small" label="End Date" type="date" value={end} onChange={e=>setEnd(e.target.value)} InputLabelProps={{shrink:true}}/>
      </div>
      <div style={{marginBottom:8,fontSize:13}}>
        Rotations: {total} | Failures: {failures} | Last Failure: {lastFail ? `${lastFail.timestamp} (${lastFail.key}: ${lastFail.status})` : 'None'}
      </div>
      <div style={{display: 'flex', gap: 4}}>
        {days.map(day => (
          <Tooltip key={day} title={
            <div>
              <strong>{day}</strong><br/>
              {byDay[day].map((e, i) => (
                <div key={i}>{e.key}: {e.status}</div>
              ))}
            </div>
          }>
            <div style={{
              width: 18, height: 36, background: getColor(byDay[day].some(e => e.status !== 'SUCCESS') ? 'FAIL' : 'SUCCESS'),
              borderRadius: 4, border: '1px solid #888', cursor: 'pointer'
            }} />
          </Tooltip>
        ))}
      </div>
      <div style={{marginTop: 8, fontSize: 12}}>
        <span style={{background:'#4CAF50',padding:'0 8px',marginRight:4}} /> Success
        <span style={{background:'#FFC107',padding:'0 8px',margin:'0 4px'}} /> Verify Fail
        <span style={{background:'#F44336',padding:'0 8px',margin:'0 4px'}} /> Fail/Fallback
      </div>
    </div>
  );
};

export default SecretRotationHeatmap;
