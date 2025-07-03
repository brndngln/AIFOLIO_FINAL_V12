import React from 'react';
import { Bar, Pie } from 'react-chartjs-2';
import { Chart, registerables } from 'chart.js';
Chart.register(...registerables);

export function EventTypePie({ events }) {
  const counts = {};
  events.forEach(ev => { counts[ev.event] = (counts[ev.event]||0)+1; });
  return <Pie data={{
    labels: Object.keys(counts),
    datasets: [{ data: Object.values(counts), backgroundColor: ['#36a2eb','#ff6384','#ffce56','#4bc0c0','#9966ff','#ff9f40'] }]
  }} />;
}

export function ErrorBar({ events }) {
  const byType = {};
  events.forEach(ev => {
    const type = ev.event;
    byType[type] = byType[type] || { total:0, errors:0 };
    byType[type].total += 1;
    if(ev.errors && ev.errors.length) byType[type].errors += 1;
  });
  return <Bar data={{
    labels: Object.keys(byType),
    datasets: [
      { label: 'Total', data: Object.values(byType).map(x=>x.total), backgroundColor:'#36a2eb' },
      { label: 'Errors', data: Object.values(byType).map(x=>x.errors), backgroundColor:'#ff6384' }
    ]
  }} options={{ responsive:true, plugins:{ legend:{position:'top'} } }} />;
}
