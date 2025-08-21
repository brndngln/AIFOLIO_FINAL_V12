import React from "react";
import ReactDOM from "react-dom/client";
import ThemeProvider from "../theme/ThemeProvider.jsx";
import App from "./App";
import { register as registerServiceWorker } from "./registerServiceWorker";

registerServiceWorker();

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <ThemeProvider>
      <App />
    </ThemeProvider>
  </React.StrictMode>,
);
