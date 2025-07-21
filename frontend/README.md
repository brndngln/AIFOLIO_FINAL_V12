# AIFOLIO™ SAFE AI Dashboard — BUSINESS MODE (React PWA)

This is the static, deterministic, OWNER-controlled React frontend for AIFOLIO™ FINAL_V12, optimized for secure SAFE AI PDF vault business operations. All features are lean, static, and business-only — no backend, no adaptive logic, no global/public features.

---

## 🚀 Getting Started (OWNER/Business)

### 1. Install Dependencies

```bash
npm install
```

### 2. Run Locally (Dev Mode)

```bash
npm run dev
```

App runs at [http://localhost:3000](http://localhost:3000).

### 3. Install as PWA

- Open in Chrome/Safari/Edge (Mac or phone)
- Click “Add to Home Screen” for full-screen, offline PWA experience
- Replace `public/icon-192.png` and `icon-512.png` with your AIFOLIO™ icons for branding

### 4. Build for Production

```bash
npm run build
```

- Output is static, ready for Netlify/Vercel/static hosts

### 5. Sample/Test Vaults

- Sample test vaults and metadata are in `src/sample-data/`
- Use these for onboarding, demos, or UI tests

### 6. Policy Docs & Onboarding

- Terms of Service, Refund Policy, and Privacy Policy are fully integrated, collapsible, and OWNER-controlled in-app (see “Policy Documents” panel)
- All policy docs are static, business-focused, and GDPR/CCPA compliant

### 7. SAFE AI Compliance & Business Features

- All actions are audit-logged and OWNER-controlled
- No auto-publish, no adaptive/agentic logic
- Only batches 1–25 (business, partner, readiness) are included
- All global/treaty/public/NGO features are removed
- Safeguard, compliance, and validation layers are static and visible in dashboard

### 8. Theming & Brand

- All theme settings in `theme/theme.js` and `ThemeProvider.js`
- Dark mode enabled by default
- Brand colors, fonts, and badges included

### 9. Deployment & CI/CD

- Static build can be deployed to Netlify, Vercel, or any static host
- For CI/CD: Add your preferred workflow (GitHub Actions, Netlify CI, etc.)
- No backend or environment variables required

---

## ✅ Launch Checklist

- [ ] Replace default icons in `public/` with your AIFOLIO™ icons
- [ ] Review sample vaults in `src/sample-data/`
- [ ] Test installability as a PWA on Mac and phone
- [ ] Review all static policy docs in-app
- [ ] Confirm all business-only features are present (no global/public panels)
- [ ] Run `npm run build` and deploy to static host
- [ ] (Optional) Set up CI/CD for automated deploys

---

## 🛡️ SAFE AI Business Mode Features

- **Static, deterministic, and OWNER-controlled**
- **Policy docs:** Full Terms, Refund, and Privacy Policy (collapsible, in-app)
- **Audit logging:** All actions are UI-logged (static, visible)
- **Compliance panels:** GDPR/CCPA, tax, workflow, validation layers
- **No adaptive/agentic logic:** 100% static, no AI/ML or backend
- **Business batches 1–25 only:** No global/treaty/public/NGO
- **Future enhancements:** Static placeholders for roadmap features

---

## 🧭 OWNER Onboarding

1. Install dependencies and run locally
2. Review dashboard panels and static business checklists
3. Review and customize policy docs if needed
4. Test PWA install and offline support
5. Deploy to your preferred static host
6. Use sample vaults for demo/testing

---

**AIFOLIO™ SAFE AI BUSINESS MODE is ready for secure, compliant, and OWNER-controlled PDF vault operations.**

For custom onboarding, further UI polish, or automation, contact your SAFE AI developer or OWNER support. 7. If configured, notifications/webhooks fire (Discord, Email, Gumroad, Notion, etc). 8. User/affiliate receives the PDF via chosen channel. 9. Errors are shown with recovery steps (retry, check input, contact admin).

## ⚠️ Error Handling

- All error states are shown with clear messages.
- User can retry after fixing input or connectivity issues.
- All AI-generated text is SAFE AI-guarded and visually marked.

## 📦 Dependencies

- React 18+
- Axios
- React Router
- Styled Components or CSS Modules (see theme)
- JS/TS Testing Library (see `tests/ui_enhancements/`)

## 🤝 Partner Integrations

- Add new partner/affiliate dashboards as new components in `src/components/`.
- Use provided hooks and API structure for easy integration.

---

For more details, see inline comments in each component or contact the AIFOLIO engineering team.
