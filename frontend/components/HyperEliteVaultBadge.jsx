// HYPER ELITE VAULT BADGE UI COMPONENT (React, static, deterministic, SAFE AI)
import React from 'react';
import './HyperEliteVaultBadge.css';

export default function HyperEliteVaultBadge({ tooltip = true, external = false }) {
  return (
    <div className={`hyper-elite-vault-badge${external ? ' external' : ''}`} title={tooltip ? 'Elite AIFOLIO_FINAL_V12 Vault — Phase 200 Certified' : undefined}>
      <svg width="56" height="48" viewBox="0 0 56 48" className="badge-hexagon">
        <polygon points="28,4 52,16 52,32 28,44 4,32 4,16" fill="#FFD700" stroke="#222" strokeWidth="3" />
        <g>
          <text x="28" y="20" textAnchor="middle" fontWeight="bold" fontSize="11" fill="#222">HYPER ELITE</text>
          <text x="28" y="33" textAnchor="middle" fontWeight="bold" fontSize="12" fill="#222">VAULT</text>
        </g>
        <g>
          <path d="M18,26 Q28,10 38,26" fill="none" stroke="#222" strokeWidth="2" />
          <circle cx="28" cy="24" r="4" fill="#FFD700" stroke="#222" strokeWidth="2" />
          <polygon points="28,12 32,20 24,20" fill="#222" /> {/* Crown */}
        </g>
      </svg>
      {external && <span className="external-label">🏆 HYPER ELITE VAULT — Phase 200 Certified</span>}
      {!external && <span className="internal-label">[🏆 HYPER ELITE VAULT] (PHASE 200+)</span>}
    </div>
  );
}
