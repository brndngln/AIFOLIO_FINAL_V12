import React, { useState } from "react";

export default function NotificationSettingsUI({ config, onSave }) {
  const [settings, setSettings] = useState(config || {});

  const handleChange = (e) => {
    setSettings({ ...settings, [e.target.name]: e.target.value });
  };

  const handleCheckbox = (e) => {
    setSettings({ ...settings, [e.target.name]: e.target.checked });
  };

  return (
    <div className="notification-settings-ui">
      <h3>Notification Settings</h3>
      <div>
        <label>
          Discord Webhook URL
          <input type="text" name="discord_webhook" value={settings.discord_webhook || ""} onChange={handleChange} />
        </label>
      </div>
      <div>
        <label>
          Email To
          <input type="email" name="email_to" value={settings.email_to || ""} onChange={handleChange} />
        </label>
      </div>
      <div>
        <label>
          Gumroad URL
          <input type="text" name="gumroad_url" value={settings.gumroad_url || ""} onChange={handleChange} />
        </label>
      </div>
      <div>
        <label>
          Notion URL
          <input type="text" name="notion_url" value={settings.notion_url || ""} onChange={handleChange} />
        </label>
      </div>
      <div>
        <label>
          Custom Webhook
          <input type="text" name="custom_webhook" value={settings.custom_webhook || ""} onChange={handleChange} />
        </label>
      </div>
      <button onClick={() => onSave(settings)}>Save Settings</button>
    </div>
  );
}
