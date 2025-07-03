import React, { useEffect, useState } from "react";

// Placeholder for backend API
const fetchLeaderboard = async () => [
  { rank: 1, vault: "BRIEFGEN", user: "admin", exports: 120 },
  { rank: 2, vault: "LUXDESIGNER", user: "designerpro", exports: 95 },
  { rank: 3, vault: "TRAFFIQ", user: "partner01", exports: 80 }
];

export default function Leaderboard() {
  const [leaders, setLeaders] = useState([]);
  useEffect(() => { fetchLeaderboard().then(setLeaders); }, []);

  return (
    <div className="leaderboard" style={{background:'#181e2b',color:'#b3e9ff',borderRadius:16,padding:32,boxShadow:'0 0 32px #00e6ff44'}}>
      <h2>Vault Leaderboard</h2>
      <table style={{width:'100%',background:'#232b3b',borderRadius:8}}>
        <thead><tr style={{color:'#00e6ff'}}><th>Rank</th><th>Vault</th><th>User</th><th>Exports</th></tr></thead>
        <tbody>
          {leaders.map(l => (
            <tr key={l.rank}><td>{l.rank}</td><td>{l.vault}</td><td>{l.user}</td><td>{l.exports}</td></tr>
          ))}
        </tbody>
      </table>
      <div style={{marginTop:32,opacity:0.8}}>
        <em>Track elite vault usage, exports, and community contributions. All stats are SAFE AI-compliant and owner-auditable.</em>
      </div>
    </div>
  );
}
