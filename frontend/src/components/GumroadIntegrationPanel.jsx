import React, { useState } from 'react';
import HyperEliteVaultBadge from '../../components/HyperEliteVaultBadge';
<<<<<<< HEAD
=======
import PropTypes from 'prop-types'; // [WINDSURF FIXED]
>>>>>>> omni_repair_backup_20250704_1335

/**
 * GumroadIntegrationPanel
 * - Displays vault preview and pricing data
 * - Allows admin approval/override
 * - Integrates with Gumroad (core focus)
 * - Placeholder for PayPal and future delivery integrations
 * - Reserved spots for analytics, performance, and AI/screenshot enhancements
 */
<<<<<<< HEAD
export default function GumroadIntegrationPanel({ vault, onApprove, onOverridePrice }) {
=======
function GumroadIntegrationPanel({ vault, onApprove, onOverridePrice }) {
>>>>>>> omni_repair_backup_20250704_1335
  const [approved, setApproved] = useState(false);
  const [overridePrice, setOverridePrice] = useState('');
  const [paypalComingSoon] = useState(true);

  if (!vault) return <div>No vault selected.</div>;

  const handleApprove = () => {
    setApproved(true);
    if (onApprove) onApprove(vault);
  };

  const handleOverride = () => {
    if (overridePrice && onOverridePrice) {
      onOverridePrice(Number(overridePrice));
    }
  };

  return (
    <div className="gumroad-panel">
      <h2 className="text-2xl font-bold mb-4">Gumroad Integration</h2>
      <div className="vault-summary mb-4 p-4 border rounded bg-gray-50">
        <h3 className="text-xl font-semibold mb-2" style={{display:'flex',alignItems:'center',gap:8}}>
  {vault.metadata.title}
  <HyperEliteVaultBadge tooltip={true} external={false} />
</h3>
        <div><strong>Niche:</strong> {vault.metadata.niche}</div>
        <div><strong>Price:</strong> ${vault.metadata.price}</div>
        <div><strong>Bundle Size:</strong> {vault.metadata.bundle_size}</div>
        <div><strong>Value Score:</strong> {vault.preview.value_score}</div>
        <div><strong>Outline:</strong> <ul>{vault.preview.outline.map((o, i) => <li key={i}>{o}</li>)}</ul></div>
        <div><strong>Testimonials:</strong> <ul>{vault.preview.testimonials.map((t, i) => <li key={i}>{t.text} <em>({t.persona})</em></li>)}</ul></div>
        <div><strong>Benefits:</strong> <ul>{vault.preview.benefits.map((b, i) => <li key={i}>{b}</li>)}</ul></div>
        <div><strong>Average Rating:</strong> {vault.preview.avg_rating} ({vault.preview.total_reviews} reviews)</div>
        <div><strong>Featured Review:</strong> {vault.preview.featured_review}</div>
        <div className="flex gap-2 mt-2">
          {vault.preview.screenshots.map((img, i) => (
            <img key={i} src={`previews/${img}`} alt={`Preview ${i+1}`} className="w-24 h-32 object-cover border" />
          ))}
        </div>
      </div>

      <div className="admin-actions mb-4">
        <button className="btn-approve mr-2" onClick={handleApprove} disabled={approved}>
          {approved ? 'Approved' : 'Approve for Gumroad'}
        </button>
        <input
          type="number"
          placeholder="Override Price"
          value={overridePrice}
          onChange={e => setOverridePrice(e.target.value)}
          className="input-price mr-2"
        />
        <button className="btn-override" onClick={handleOverride}>
          Set Override Price
        </button>
      </div>

      <div className="integration-section mb-4">
        <h4 className="font-semibold">Gumroad Delivery</h4>
        <button className="btn-gumroad" onClick={async () => {
          // Call backend API to deliver to Gumroad
          try {
            const res = await fetch('/api/gumroad-deliver', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                metadataPath: `../vaults/the_ultimate_guide_to_ai_tools_and_automation_success/metadata.json`,
                previewPath: `../vaults/the_ultimate_guide_to_ai_tools_and_automation_success/vault_preview.json`
              })
            });
            const result = await res.json();
            alert(result.success ? `Gumroad delivery successful! Product ID: ${result.productId}` : `Delivery failed: ${result.error}`);
          } catch (e) {
            alert('Delivery failed: ' + e.message);
          }
        }}>Push to Gumroad</button>
      </div>

      <div className="integration-section mb-4 opacity-60">
        <h4 className="font-semibold">PayPal Delivery</h4>
        <button className="btn-paypal" disabled>
          {paypalComingSoon ? 'PayPal Integration Coming Soon' : 'Push to PayPal'}
        </button>
      </div>

      {/* Reserved for future features: analytics, performance, AI/screenshot enhancements */}
      {/*
      <div className="future-section mb-4">
        <h4 className="font-semibold">Analytics & Performance (Coming Soon)</h4>
      </div>
      <div className="future-section mb-4">
        <h4 className="font-semibold">AI/Screenshot Enhancements (Coming Soon)</h4>
      </div>
      */}
    </div>
  );
}
<<<<<<< HEAD
=======

GumroadIntegrationPanel.propTypes = {
  vault: PropTypes.shape({
    metadata: PropTypes.shape({
      title: PropTypes.string.isRequired,
      niche: PropTypes.string,
      price: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
      bundle_size: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
    }).isRequired,
    preview: PropTypes.shape({
      value_score: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
      outline: PropTypes.arrayOf(PropTypes.string),
      testimonials: PropTypes.arrayOf(
        PropTypes.shape({
          text: PropTypes.string,
          persona: PropTypes.string
        })
      ),
      benefits: PropTypes.arrayOf(PropTypes.string),
      avg_rating: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
      total_reviews: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
      featured_review: PropTypes.string,
      screenshots: PropTypes.arrayOf(PropTypes.string)
    })
  }),
  onApprove: PropTypes.func,
  onOverridePrice: PropTypes.func
}; // [WINDSURF FIXED]

export default GumroadIntegrationPanel; // [WINDSURF FIXED]
>>>>>>> omni_repair_backup_20250704_1335
