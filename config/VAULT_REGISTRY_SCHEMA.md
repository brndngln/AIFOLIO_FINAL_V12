# Vault Registry Schema & Integration Guide

## Overview

The vault registry defines all vault modules/components for AIFOLIO, providing metadata for backend event handling, compliance, notification routing, and frontend UI integration.

## Vault Entry Fields

Each vault entry in `vault_registry.json` must include:

| Field                 | Type     | Required | Description                                                         |
| --------------------- | -------- | -------- | ------------------------------------------------------------------- |
| id                    | string   | Yes      | Unique vault identifier.                                            |
| label (title)         | string   | Yes      | Human-readable vault name.                                          |
| icon                  | string   | Yes      | Emoji or glyph for UI display.                                      |
| component             | string   | Yes      | UI/frontend component name.                                         |
| event_types           | string[] | Yes      | Supported backend event types (e.g., PDF_CREATED, VAULT_PUBLISHED). |
| compliance_profile    | string   | Yes      | Compliance profile (e.g., global, regional, restricted).            |
| notification_channels | string[] | Yes      | Notification channels (discord, telegram, sms, email, webhook).     |
| founder_controlled    | boolean  | Yes      | If true, only founder/admin can modify.                             |
| niche                 | string   | Yes      | Vault's focus area or specialization.                               |
| description           | string   | Yes      | Detailed description of vault's function and use cases.             |

**Note:** User/runtime-specific fields like `owner_email` and `alert_email_opt_in` are not part of the static registry.

## Example Entry

```json
{
  "id": "templiq_templates",
  "label": "TEMPLIQ™",
  "icon": "🧾",
  "component": "TEMPLIQ",
  "event_types": ["PDF_CREATED", "VAULT_PUBLISHED", "COMPLIANCE_AUDIT"],
  "compliance_profile": "global",
  "notification_channels": ["discord", "telegram", "sms", "email", "webhook"],
  "founder_controlled": true,
  "niche": "templates",
  "description": "Automated template and course generator for business, education, and productivity."
}
```

## Integration Points

- **Backend:** Event listeners require `id`, `title` (label), `niche`, `description`, compliance and notification fields.
- **Frontend:** UI components bind to registry fields for display and event triggering.
- **Compliance:** Compliance workflows use `compliance_profile`, `niche`, and `description` for checks.
- **Notification:** Channels listed in `notification_channels` are used for alerts and updates.

## Compliance & Testing

- All vaults must pass compliance checks on creation and update.
- Automated tests verify presence and correct handling of all required fields.
- Pattern-aware simulation system tests vault event flows and anti-sentience safeguards.

## Changelog

- **2025-06-24:** Added `niche` and `description` fields. Updated backend, frontend, and test coverage accordingly.

---

For further details, see backend event listeners and test modules related to vaults.
