import React, { useState } from "react";
import axios from "axios";

const initialState = {
  partner: "",
  certification_status: "Pending",
  expiry_date: "",
  last_audit: "",
  terms_file: null,
  contact_email: "",
  notes: ""
};

export default function PartnerCertificationForm({ onExport }) {
  const [form, setForm] = useState(initialState);
  const [status, setStatus] = useState("");
  const [submitting, setSubmitting] = useState(false);

  function handleChange(e) {
    const { name, value, files } = e.target;
    setForm(f => ({
      ...f,
      [name]: files ? files[0] : value
    }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setSubmitting(true);
    try {
      const payload = { ...form, terms_file: undefined };
      await axios.post("/batch-scaling/partner-certifications", payload);
      setStatus("Certification submitted.");
    } catch (err) {
      setStatus("Error submitting: " + err.message);
    }
    setSubmitting(false);
  }

  function handleExport(type) {
    if (onExport) onExport(type, form.partner);
  }

  return (
    <form className="partner-cert-form" onSubmit={handleSubmit}>
      <h3>Partner Certification</h3>
      <label>Partner Name<input name="partner" value={form.partner} onChange={handleChange} required /></label>
      <label>Status
        <select name="certification_status" value={form.certification_status} onChange={handleChange}>
          <option>Pending</option>
          <option>Approved</option>
          <option>Expired</option>
        </select>
      </label>
      <label>Certification Expiry Date<input name="expiry_date" type="date" value={form.expiry_date} onChange={handleChange} /></label>
      <label>Last Audit Date<input name="last_audit" type="date" value={form.last_audit} onChange={handleChange} /></label>
      <label>Upload Partner Terms (PDF)<input name="terms_file" type="file" accept="application/pdf" onChange={handleChange} /></label>
      <label>Partner Contact Email<input name="contact_email" type="email" value={form.contact_email} onChange={handleChange} /></label>
      <label>Internal Notes<textarea name="notes" value={form.notes} onChange={handleChange} /></label>
      <div style={{marginTop:8}}>
        <button type="submit" disabled={submitting}>Submit Certification</button>
        <button type="button" onClick={() => handleExport('pdf')}>Export PDF</button>
        <button type="button" onClick={() => handleExport('csv')}>Export CSV</button>
      </div>
      <div className="status">{status}</div>
    </form>
  );
}
