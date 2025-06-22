import React, { useState } from "react";

export default function PDFBuilderSettings({ config, onSave }) {
  const [settings, setSettings] = useState(config || {});

  const handleChange = (e) => {
    setSettings({ ...settings, [e.target.name]: e.target.value });
  };

  return (
    <div className="pdf-builder-settings">
      <h3>PDF Builder Settings</h3>
      <div>
        <label>
          Default Output Directory
          <input type="text" name="output_dir" value={settings.output_dir || "vaults"} onChange={handleChange} />
        </label>
      </div>
      <div>
        <label>
          Default Template
          <input type="text" name="template" value={settings.template || "vault_template.html"} onChange={handleChange} />
        </label>
      </div>
      <button onClick={() => onSave(settings)}>Save Settings</button>
    </div>
  );
}
