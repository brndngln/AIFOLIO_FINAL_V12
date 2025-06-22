# AIFOLIO™ SAFE AI Dashboard — React Frontend

This is the React-based frontend for AIFOLIO_FINAL_V12, providing a secure, brand-consistent interface for SAFE AI PDF generation, audit, and partner/affiliate management.

## 🚀 Getting Started

### 1. Install Dependencies
```
npm install
```

### 2. Run Locally (Dev Mode)
```
npm start
```
The app will run at [http://localhost:3000](http://localhost:3000) by default.

### 3. Connect to Backend
- By default, API requests are proxied to the backend at `http://localhost:8000`.
- To change the backend URL, update the `proxy` field in `package.json` or set up a `.env` file with `REACT_APP_API_URL`.

### 4. Build for Production
```
npm run build
```
The production build will be in the `build/` directory.

### 5. Update Styles & Theme
- Edit `frontend/theme/theme.js` and `frontend/theme/ThemeProvider.js` for colors, fonts, and layout.
- See Theming section below for details.

### 6. Add New PDF Builder Buttons
- Edit `src/components/PDFBuilderDashboard.jsx`:
  - Add a new entry to the `PDF_BUILDERS` array with the correct endpoint key and label.
  - Add any required input fields for new PDF types.

### 7. Frontend Testing
- JS/TS tests are in `tests/ui_enhancements/` (see memory: do NOT convert to Python).
- Run tests with:
```
npm test
```

## 🖌️ Theming & Brand Configuration

- All theme settings are in `frontend/theme/theme.js` and provided via `ThemeProvider.js`.
- **Dark Mode:** Enabled by default, using AIFOLIO™ brand palette.
- **Fonts:** Uses `Inter`, `Roboto`, and PDF branding fonts (see theme.js).
- **Buttons/Progress:** Styled with brand color, rounded, animated progress.
- **SAFE AI Compliance:** Visual badges (`.safe-ai-badge`), banners, and status indicators are styled in `theme.js` and `theme.css`.
- To change theme, edit `theme.js` and restart the dev server.

## 🧭 UI Workflow: Generate PDF

1. User logs in and navigates to Dashboard.
2. In the "Generate PDF" section, user selects a PDF type and fills in required fields.
3. User clicks the PDF builder button.
4. UI shows loading/progress state.
5. Backend generates PDF (SAFE AI-guarded).
6. On success, UI displays a confirmation, a download link, and a "SAFE AI Verified" badge.
7. If configured, notifications/webhooks fire (Discord, Email, Gumroad, Notion, etc).
8. User/affiliate receives the PDF via chosen channel.
9. Errors are shown with recovery steps (retry, check input, contact admin).

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
