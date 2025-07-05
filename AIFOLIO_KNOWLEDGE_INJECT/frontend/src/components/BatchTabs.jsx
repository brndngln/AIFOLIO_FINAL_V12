import React, { useState } from "react";
import Batch21FederatedTrustPanel from "./Batch21FederatedTrustPanel";
import Batch22CertificationLegalPanel from "./Batch22CertificationLegalPanel";
import Batch23GlobalPublicReadinessPanel from "./Batch23GlobalPublicReadinessPanel";
import Batch24EnterprisePublicScalePanel from "./Batch24EnterprisePublicScalePanel";
import Batch25FinalTrustCertificationPanel from "./Batch25FinalTrustCertificationPanel";

const BATCHES = [
  { key: "21", label: "Batch 21: Federated Trust", component: Batch21FederatedTrustPanel },
  { key: "22", label: "Batch 22: Certification & Legal", component: Batch22CertificationLegalPanel },
  { key: "23", label: "Batch 23: Global Readiness", component: Batch23GlobalPublicReadinessPanel },
  { key: "24", label: "Batch 24: Enterprise Scale", component: Batch24EnterprisePublicScalePanel },
  { key: "25", label: "Batch 25: Final Trust", component: Batch25FinalTrustCertificationPanel }
];

export default function BatchTabs() {
  const [tab, setTab] = useState(BATCHES[0].key);
  const CurrentPanel = BATCHES.find(b => b.key === tab).component;
  return (
    <section className="batch-tabs" aria-label="Batch Modules" tabIndex={0}>
      <nav style={{display:'flex',gap:8,marginBottom:16}}>
        {BATCHES.map(b => (
          <button
            key={b.key}
            onClick={() => setTab(b.key)}
            style={{
              padding:'8px 18px',
              borderRadius:6,
              border:'none',
              background: tab === b.key ? '#2563eb' : '#e0e7ef',
              color: tab === b.key ? '#fff' : '#0f172a',
              fontWeight:600,
              fontSize:15
            }}
            aria-selected={tab === b.key}
          >
            {b.label}
          </button>
        ))}
      </nav>
      <div>
        <CurrentPanel />
      </div>
    </section>
  );
}
