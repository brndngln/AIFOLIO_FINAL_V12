import React, { useState } from "react";
import axios from "axios";

const PDF_BUILDERS = [
  { key: "niche-product", label: "Niche Product PDF" },
  { key: "affiliate-promo", label: "Affiliate Promo Pack" },
  { key: "social-media", label: "Social Media Content Pack" },
  { key: "market-trends", label: "AI Market Trends Report" },
  { key: "revenue-conversion", label: "AI Revenue & Conversion Report" },
  { key: "customer-welcome", label: "Customer Welcome Pack" },
  { key: "niche-ebook", label: "Niche Authority eBook" },
  { key: "email-funnel-blueprint", label: "Email Funnel Blueprint" }
];

const initialState = {
  loading: false,
  success: false,
  error: null,
  downloadLink: null,
  activeBuilder: null
};

export default function PDFBuilderDashboard({ token }) {
  const [state, setState] = useState(initialState);
  const [formData, setFormData] = useState({});

  const handleInputChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleGenerate = async (key) => {
    setState({ ...initialState, loading: true, activeBuilder: key });
    try {
      // TODO: Replace with actual data collection UI per builder
      const payload = { data: formData };
      const res = await axios.post(
        `/pdf/${key}`,
        payload,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setState({ ...initialState, success: true, downloadLink: res.data, activeBuilder: key });
    } catch (err) {
      setState({ ...initialState, error: err.response?.data?.detail || err.message, activeBuilder: key });
    }
  };

  return (
    <div className="pdf-builder-dashboard">
      <h2>Generate PDF</h2>
      <div className="pdf-builder-buttons">
        {PDF_BUILDERS.map((builder) => (
          <button
            key={builder.key}
            onClick={() => handleGenerate(builder.key)}
            disabled={state.loading && state.activeBuilder === builder.key}
            className="pdf-builder-btn"
          >
            {state.loading && state.activeBuilder === builder.key ? "Generating..." : builder.label}
          </button>
        ))}
      </div>
      {/* Example: Add input fields for required data */}
      <div className="pdf-builder-form">
        <input
          type="text"
          name="catalog_title"
          placeholder="Catalog Title (example)"
          value={formData.catalog_title || ""}
          onChange={handleInputChange}
        />
        {/* Add more fields as needed per PDF type */}
      </div>
      {state.success && (
        <div className="pdf-success">
          <span role="img" aria-label="success">✅</span> PDF generated!
          <a href={`/${state.downloadLink}`} target="_blank" rel="noopener noreferrer">View Download Link</a>
          <span className="safe-ai-badge">SAFE AI Verified</span>
        </div>
      )}
      {state.error && (
        <div className="pdf-error">{state.error}</div>
      )}
    </div>
  );
}
