import React, { useState, useEffect } from 'react';
import AnalyticsDashboard from './components/AnalyticsDashboard';
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

import BatchTabs1to16 from "./components/BatchTabs1to16";
import BatchTabs from "./components/BatchTabs";
import PartnerCertificationExportPanel from "./components/PartnerCertificationExportPanel";



import ThemeProvider from '../theme/ThemeProvider.jsx';

import GumroadIntegrationPanel from './components/GumroadIntegrationPanel';

// Utility to load vault data from public (stub for real API)
function loadLatestVault() {
  // In a real app, fetch from backend or API
  try {
    // eslint-disable-next-line no-undef
    const preview = require('../vaults/the_ultimate_guide_to_ai_tools_and_automation_success/vault_preview.json');
    // eslint-disable-next-line no-undef
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
          <div className="flex justify-between items-center mb-8">
            <h1 className="text-4xl font-bold" style={{
              color: 'var(--text)',
              backgroundColor: 'var(--accent)',
              padding: 'var(--spacing-md)',
              borderRadius: 'var(--border-radius-md)',
              boxShadow: 'var(--shadow-sm)'
            }}>AIFOLIO™</h1>
            <div className="flex space-x-4">
              <button className="theme-button">
                Theme
              </button>
              <button className="theme-button">
                Settings
              </button>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="theme-panel">
              <h2 className="text-2xl font-bold mb-4" style={{
                color: 'var(--text)',
                backgroundColor: 'var(--accent)',
                padding: 'var(--spacing-md)',
                borderRadius: 'var(--border-radius-md)'
              }}>Analytics Dashboard</h2>
              <AnalyticsDashboard />
            </div>
            <div className="theme-panel col-span-2">
              <GumroadIntegrationPanel
                vault={vault}
                onApprove={handleApprove}
                onOverridePrice={handleOverridePrice}
              />
            </div>
          </div>

          {/* Reserved for future features: analytics, performance, AI/screenshot enhancements */}
          {/*
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mt-8">
            <div className="theme-panel">
              <h2 className="text-2xl font-bold mb-4" style={{
                color: 'var(--text)',
                backgroundColor: 'var(--accent)',
                padding: 'var(--spacing-md)',
                borderRadius: 'var(--border-radius-md)'
              }}>Analytics & Performance (Coming Soon)</h2>
            </div>
            <div className="theme-panel">
              <h2 className="text-2xl font-bold mb-4" style={{
                color: 'var(--text)',
                backgroundColor: 'var(--accent)',
                padding: 'var(--spacing-md)',
                borderRadius: 'var(--border-radius-md)'
              }}>AI/Screenshot Enhancements (Coming Soon)</h2>
            </div>
          </div>
          {/* Partner Certification Export Section */}
          <div className="theme-panel mt-8" style={{background:'#f3f4f6',borderRadius:12,padding:24,marginBottom:32}}>
            <h2 className="text-xl font-bold mb-4" style={{color:'#0f172a'}}>Partner Certification Export</h2>
            <PartnerCertificationExportPanel />
          </div>

          {/* SAFE AI OWNER CONTROL PANEL */}
          <div className="theme-panel mt-12" style={{background:'#fff',borderRadius:12,padding:32,marginBottom:32}}>
            <OwnerControlPanel auditLog={[]} onExport={()=>{}} onChecklistExport={()=>{}} />
          </div>

          {/* SAFE AI BUSINESS CHECKLISTS & PIPELINE */}
          <div className="theme-panel mt-12" style={{background:'#f8fafc',borderRadius:12,padding:24,marginBottom:32}}>
            <h2 className="text-2xl font-bold mb-4" style={{color:'#0f172a'}}>SAFE AI Business Checklists & Pipeline</h2>
            <CompletionChecklist />
            <ReadinessChecklist />
            <UXBestPractices />
            <SafeAIMistakesToAvoid />
            <SafeAIStaticLogicSuggestions />
            <InnovationPipeline />
            <SafeguardValidationLayer />
            <ComplianceWorkflowStack />
            <PolicyDocuments />
            <FutureStaticEnhancements />
            <BeginnerMistakesToAvoid />
          </div>
        </div>

          

          {/* SAFE AI Checklists & Playbook */}
          <div className="theme-panel mt-12" style={{background:'#f3f4f6',borderRadius:12,padding:32,marginBottom:32}}>
            <CompletionChecklist />
            <ReadinessChecklist />
            <UXBestPractices />
            
          </div>

        {/* SAFE AI Checklists & Playbook */}
        <div className="theme-panel mt-12" style={{background:'#f3f4f6',borderRadius:12,padding:32,marginBottom:32}}>
          <CompletionChecklist />
          <ReadinessChecklist />
          <UXBestPractices />
          
        </div>

        {/* SAFE AI Static Logic Suggestions (Future, Static) */}
        <div className="theme-panel mt-12" style={{background:'#fff',borderRadius:12,padding:32,marginBottom:32}}>
          <SafeAIStaticLogicSuggestions />
        </div>
      </div>
    </ThemeProvider>
  );
}

export default App;
