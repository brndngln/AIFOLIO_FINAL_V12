import React from "react";
import OwnerAuditLogViewerPanel from "./OwnerAuditLogViewerPanel";
import OwnerControlPanel from "./OwnerControlPanel";
import SmartPricingEnginePanel from "./SmartPricingEnginePanel";
import ShowcaseEnginePanel from "./ShowcaseEnginePanel";
import ComplianceExportsPanel from "./ComplianceExportsPanel";
import SafeguardValidationLayer from "./SafeguardValidationLayer";
import AnalyticsDashboard from "./AnalyticsDashboard";
import StaticBundleRecommendationPanel from "./StaticBundleRecommendationPanel";
import GDPRDashboardPanel from "./GDPRDashboardPanel";
import FutureStaticEnhancements from "./FutureStaticEnhancements";
import { Tabs, Tab, Box, Typography } from "@mui/material";

const panels = [
  { label: "Audit Log", component: <OwnerAuditLogViewerPanel /> },
  { label: "Owner Controls", component: <OwnerControlPanel /> },
  { label: "Pricing", component: <SmartPricingEnginePanel /> },
  { label: "Showcase", component: <ShowcaseEnginePanel /> },
  { label: "Compliance", component: <ComplianceExportsPanel /> },
  { label: "Validation", component: <SafeguardValidationLayer /> },
  { label: "Analytics", component: <AnalyticsDashboard /> },
  {
    label: "Bundle Recommender",
    component: <StaticBundleRecommendationPanel />,
  },
  { label: "GDPR Dashboard", component: <GDPRDashboardPanel /> },
  { label: "Future Enhancements", component: <FutureStaticEnhancements /> },
];

function SafeAIDashboard() {
  const [tab, setTab] = React.useState(0);
  return (
    <Box sx={{ width: "100%", bgcolor: "background.paper" }}>
      <Typography variant="h4" sx={{ m: 2 }}>
        SAFE AI Business System Dashboard
      </Typography>
      <Tabs
        value={tab}
        onChange={(_, v) => setTab(v)}
        variant="scrollable"
        scrollButtons="auto"
        aria-label="SAFE AI Dashboard Tabs"
        sx={{ mb: 2 }}
      >
        {panels.map((p, i) => (
          <Tab key={p.label} label={p.label} />
        ))}
      </Tabs>
      <Box sx={{ p: 2 }}>{panels[tab].component}</Box>
    </Box>
  );
}

export default SafeAIDashboard;
