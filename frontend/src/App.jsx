import React, { useState, useEffect } from 'react';
import AnalyticsDashboard from './components/AnalyticsDashboard';
import SafeAIDashboard from './components/SafeAIDashboard';
import OwnerControlPanel from "./components/OwnerControlPanel";
import CompletionChecklist from "./components/CompletionChecklist";
import ReadinessChecklist from "./components/ReadinessChecklist";
import UXBestPractices from "./components/UXBestPractices";
import SafeAIStaticLogicSuggestions from "./components/SafeAIStaticLogicSuggestions";
import SafeAIMistakesToAvoid from "./components/SafeAIMistakesToAvoid";
import InnovationPipeline from "./components/InnovationPipeline";
import SafeguardValidationLayer from "./components/SafeguardValidationLayer";
import ComplianceWorkflowStack from "./components/ComplianceWorkflowStack";
import PolicyDocuments from "./components/PolicyDocuments";
import FutureStaticEnhancements from "./components/FutureStaticEnhancements";
import BeginnerMistakesToAvoid from "./components/BeginnerMistakesToAvoid";
import OnboardingPanel from "./components/OnboardingPanel";
import FirstStepsChecklist from "./components/FirstStepsChecklist";
import AccessibilityBestPractices from "./components/AccessibilityBestPractices";
import SupportPanel from "./components/SupportPanel";
import LaunchReadinessChecklist from "./components/LaunchReadinessChecklist";
import FAQPanel from "./components/FAQPanel";
import ReleaseNotesPanel from "./components/ReleaseNotesPanel";
import ShowcaseEnginePanel from "./components/ShowcaseEnginePanel";
import SmartPricingEnginePanel from "./components/SmartPricingEnginePanel";
import PriceTestingEnginePanel from "./components/PriceTestingEnginePanel";
import ComplianceExportsPanel from "./components/ComplianceExportsPanel";
import StaticBundleRecommendationPanel from "./components/StaticBundleRecommendationPanel";
import ProductLifecycleTrackerPanel from "./components/ProductLifecycleTrackerPanel";
import GDPRDashboardPanel from "./components/GDPRDashboardPanel";
import AffiliateCampaignROIPanel from "./components/AffiliateCampaignROIPanel";
import UpcomingVaultsPipelinePanel from "./components/UpcomingVaultsPipelinePanel";
import LowPerformerAutoFlagPanel from "./components/LowPerformerAutoFlagPanel";
import AudienceInterestHeatmapPanel from "./components/AudienceInterestHeatmapPanel";
import EmailHealthReportPanel from "./components/EmailHealthReportPanel";
import TaxFilingCalendarPanel from "./components/TaxFilingCalendarPanel";
import OwnerOnboardingPanel from "./components/OwnerOnboardingPanel";
import OwnerExportAllDataPanel from "./components/OwnerExportAllDataPanel";
import OwnerHelpSupportPanel from "./components/OwnerHelpSupportPanel";
import OwnerReleaseNotesPanel from "./components/OwnerReleaseNotesPanel";
import OwnerAccessibilityChecklistPanel from "./components/OwnerAccessibilityChecklistPanel";
import OwnerBrandCustomizationPanel from "./components/OwnerBrandCustomizationPanel";
import OwnerDemoModePanel from "./components/OwnerDemoModePanel";
import OwnerBackupRestorePanel from "./components/OwnerBackupRestorePanel";
import OwnerAuditLogViewerPanel from "./components/OwnerAuditLogViewerPanel";
import NewCountryTaxLawsWatchPanel from "./components/NewCountryTaxLawsWatchPanel";
import AIGuardIntegrityMonitorPanel from "./components/AIGuardIntegrityMonitorPanel";

import BatchTabs1to16 from "./components/BatchTabs1to16";
import BatchTabs from "./components/BatchTabs";
import PartnerCertificationExportPanel from "./components/PartnerCertificationExportPanel";

import ThemeProvider from '../theme/ThemeProvider.jsx';
import GumroadIntegrationPanel from './components/GumroadIntegrationPanel';

// Utility to load vault data from public (stub for real API)
function loadLatestVault() {
  // In a real app, fetch from backend or API
  try {

    const preview = require('../vaults/the_ultimate_guide_to_ai_tools_and_automation_success/vault_preview.json');

    const metadata = require('../vaults/the_ultimate_guide_to_ai_tools_and_automation_success/metadata.json');
    return { preview, metadata };
  } catch (e) {
    return null;
  }
}

function App() {
  const vault = loadLatestVault();
  // Admin action stubs
  const handleApprove = (vault) => {
    alert('Vault approved for Gumroad!');
  };
  const handleOverridePrice = (price) => {
    alert('Override price set to $' + price);
  };
  return (
    <ThemeProvider>
      <div className="min-h-screen" style={{
        backgroundColor: 'var(--bg)',
        color: 'var(--text)'
      }}>
        <div className="container mx-auto px-4 py-8">
          {/* SAFE AI Business System Dashboard - Unified Entry Point */}
          <SafeAIDashboard />
          {/* Optionally, retain legacy panels below for reference or phased migration */}
          {/*
          <OnboardingPanel />
          <FirstStepsChecklist />
          <LaunchReadinessChecklist />
          <AccessibilityBestPractices />
          <SupportPanel />
          <FAQPanel />
          <ReleaseNotesPanel />
          <ShowcaseEnginePanel />
          <VaultPreviewCompilerPanel />
          <main style={{maxWidth:900,margin:"40px auto",padding:24}}>
            <DashboardHeader />
            <nav aria-label="OWNER quick navigation" style={{display:'flex',gap:10,marginBottom:32,flexWrap:'wrap'}}>
              <a href="#onboarding" style={{color:'#0ea5e9',fontWeight:700}}>Onboarding</a>
              <a href="#export" style={{color:'#0ea5e9',fontWeight:700}}>Export All Data</a>
              <a href="#backup" style={{color:'#0ea5e9',fontWeight:700}}>Backup/Restore</a>
              <a href="#audit" style={{color:'#0ea5e9',fontWeight:700}}>Audit Log</a>
              <a href="#demo" style={{color:'#0ea5e9',fontWeight:700}}>Demo Mode</a>
              <a href="#help" style={{color:'#0ea5e9',fontWeight:700}}>Help & Support</a>
              <a href="#release" style={{color:'#0ea5e9',fontWeight:700}}>Release Notes</a>
              <a href="#accessibility" style={{color:'#0ea5e9',fontWeight:700}}>Accessibility</a>
              <a href="#brand" style={{color:'#0ea5e9',fontWeight:700}}>Brand Customization</a>
            </nav>
            <section id="onboarding"><OwnerOnboardingPanel /></section>
            <section id="export"><OwnerExportAllDataPanel /></section>
            <section id="backup"><OwnerBackupRestorePanel /></section>
            <section id="audit"><OwnerAuditLogViewerPanel /></section>
            <section id="demo"><OwnerDemoModePanel /></section>
          </main>
          */}
        </div>
      </div>
    </ThemeProvider>
  );
}

export default App;
