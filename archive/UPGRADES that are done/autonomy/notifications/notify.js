export const notifyAdmin = (type, message) => {
  const allowedTypes = [
    "ethics_warning",
    "legal_alert",
    "upload_success",
    "auto_fix_applied",
  ];
  if (!allowedTypes.includes(type)) return;

  const alerts = {
    ethics_warning: "[🚨 ETHICS WARNING]",
    legal_alert: "[⚖️ LEGAL ALERT]",
    upload_success: "[✅ UPLOAD SUCCESS]",
    auto_fix_applied: "[🧠 AUTO-FIXED]",
  };

  console.log(alerts[type], message);
};
