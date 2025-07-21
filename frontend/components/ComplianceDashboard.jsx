import React from "react";
import { Box, Typography, Grid } from "@mui/material";
import ComplianceFeedPanel from "./ComplianceFeedPanel";
import PolicyMappingPanel from "./PolicyMappingPanel";
import ComplianceGapPanel from "./ComplianceGapPanel";
import RemediationRecommendationsPanel from "./RemediationRecommendationsPanel";
import RemediationWorkflowPanel from "./RemediationWorkflowPanel";
import ReviewerAnalyticsPanel from "./ReviewerAnalyticsPanel";

const ComplianceDashboard = ({ adminId }) => (
  <Box sx={{ p: 3, bgcolor: "#eaeaea", borderRadius: 2, mb: 2 }}>
    <Typography variant="h4" mb={3}>
      Elite Compliance Dashboard
    </Typography>
    <Grid container spacing={3}>
      <Grid item xs={12} md={6}>
        <ComplianceFeedPanel />
      </Grid>
      <Grid item xs={12} md={6}>
        <PolicyMappingPanel />
      </Grid>
      <Grid item xs={12} md={6}>
        <ComplianceGapPanel />
      </Grid>
      <Grid item xs={12} md={6}>
        <RemediationRecommendationsPanel />
      </Grid>
      <Grid item xs={12} md={12}>
        <RemediationWorkflowPanel adminId={adminId} />
      </Grid>
      <Grid item xs={12} md={12}>
        <ReviewerAnalyticsPanel />
      </Grid>
    </Grid>
  </Box>
);
export default ComplianceDashboard;
