// AIFOLIO SAFE AI Compliance & Legal Controls Component
// Enforces legal policy confirmation and receipt delivery in Vault Checkout/Publish flows
import React, { useState } from 'react';

export default function ComplianceControls({ onConfirm, onReceipt }) {
  const [policyConfirmed, setPolicyConfirmed] = useState(false);
  const [receiptSent, setReceiptSent] = useState(false);

  return (
    <div>
      <label>
        <input
          type="checkbox"
          checked={policyConfirmed}
          onChange={e => {
            setPolicyConfirmed(e.target.checked);
            if (e.target.checked && onConfirm) onConfirm();
          }}
        />
        I confirm I have read and accept the legal policy.
      </label>
      <button
        disabled={!policyConfirmed || receiptSent}
        onClick={() => {
          setReceiptSent(true);
          if (onReceipt) onReceipt();
        }}
      >
        Send Receipt
      </button>
      {receiptSent && <span>Receipt sent and logged for audit.</span>}
    </div>
  );
}
