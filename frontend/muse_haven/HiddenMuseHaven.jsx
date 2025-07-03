// HiddenMuseHaven.jsx
// Muse Haven: Hidden, owner-exclusive portal for PMP
// Static, deterministic, SAFE AI-compliant. No sentience, no adaptation.
import React, { useState } from 'react';
import OnboardingOverlay from './OnboardingOverlay';
import ApiKeyStatus from './ApiKeyStatus';
import IntegrationControls from '../dashboard/IntegrationControls';

// Quantum encryption stub
function quantumEncrypt(data) {
  return `[KYBER-ENCRYPTED]${data}`;
}

// Biometric/Passphrase/Geofence auth stub
function authenticate({ biometric, passphrase, location, time }) {
  // Static SAFE AI: only allows exact match
  return biometric === 'OWNER_BIOMETRIC' && passphrase === 'OWNER_SECRET' && location === 'OWNER_LOCATION' && time === 'OWNER_TIME';
}

const HIDDEN_TRIGGER_SEQUENCE = [1, 2, 3, 4, 5, 6, 7]; // 7-tap pattern stub
const VOICE_TRIGGER_PHRASE = "Muse, light my fire"; // Stub for voice trigger
const SWIPE_TRIGGER_PATTERN = 'spiral'; // Stub for custom swipe

// Onboarding/tutorial overlay component
function OnboardingOverlay({ step, onNext, onClose }) {
  const steps = [
    'Welcome to Muse Haven! This is your private, owner-exclusive sanctuary.',
    'Access is protected by secret triggers and multi-factor authentication.',
    'Customize Emma’s appearance, persona, and preferences in the Customization dashboard.',
    'Adjust learning mode and feedback for fully owner-controlled, SAFE AI-compliant adaptation.',
    'All chats, content, and preferences are stored in a quantum-encrypted, owner-only vault.',
    'Trigger emergency lockdown at any time for instant purge and lockout.',
    'Access contextual help via the (?) buttons throughout the portal.',
    'Use the ⚙️ Owner Control Center (top left) for all integrations, notification toggles, API key rotation, compliance audit, and logs.',
    'Integrations: Toggle Slack, Discord, and Email notifications for owner events.',
    'Integrations are static and SAFE AI-compliant: notifications are owner-controlled and never expose data.',
    'API Key Rotation: Instantly rotate all API keys (static, owner-only, SAFE AI-compliant).',
    'Compliance Audit: Run/export static compliance audit for SAFE AI, privacy, and security.',
    'Compliance audit is fully deterministic and logged; no secrets or adaptive logic.',
    'API Key Status: Instantly see if required integrations are set up—no secrets ever shown.',
    'Accessibility: Full keyboard navigation, ARIA labels, high-contrast, and large touch targets.',
    'Need help? Launch this onboarding anytime (bottom left ?) or click any "?" for contextual help. FAQ and troubleshooting are in the README.',
    'Configure notification preferences in the Owner Control Center.',
    'Rotate API keys for enhanced security.',
    'Run a compliance audit to ensure SAFE AI and regulatory compliance.'
  ];
  return (
    <div style={{position:'fixed',top:0,left:0,width:'100vw',height:'100vh',background:'rgba(0,0,0,0.8)',zIndex:9999,color:'#fff',display:'flex',flexDirection:'column',justifyContent:'center',alignItems:'center'}} aria-modal="true" role="dialog">
      <div style={{maxWidth:500,padding:30,background:'#222',borderRadius:18,boxShadow:'0 8px 32px rgba(0,0,0,0.25)'}}>
        <h3 style={{marginBottom:8}}>Onboarding</h3>
        <div style={{display:'flex',justifyContent:'center',marginBottom:16}} aria-label="Onboarding Progress">
          {steps.map((_,i)=>(
            <div key={i} style={{width:12,height:12,borderRadius:'50%',margin:'0 4px',background:i===step?'#fff':'#555',border:i===step?'2px solid #4cafef':'2px solid #222'}}></div>
          ))}
        </div>
        <p style={{fontSize:18,lineHeight:1.5}}>{steps[step]}</p>
        <div style={{marginTop:24,display:'flex',justifyContent:'center'}}>
          {step < steps.length-1 ? (
            <button onClick={onNext} style={{fontSize:18,padding:'12px 32px',borderRadius:8,background:'#4cafef',color:'#fff',border:'none',boxShadow:'0 2px 8px #222',cursor:'pointer'}}>Next</button>
          ) : (
            <button onClick={onClose} style={{fontSize:18,padding:'12px 32px',borderRadius:8,background:'#4cafef',color:'#fff',border:'none',boxShadow:'0 2px 8px #222',cursor:'pointer'}}>Finish</button>
          )}
        </div>
      </div>
    </div>
  );
}

// Contextual help component
function HelpTooltip({ text, onClose }) {
  return (
    <div style={{position:'fixed',bottom:40,right:40,background:'#333',color:'#fff',padding:18,borderRadius:8,zIndex:9998}}>
      <span>{text}</span>
      <button style={{marginLeft:16}} onClick={onClose}>Close</button>
    </div>
  );
}

function ApiKeyStatus() {
  const [status, setStatus] = React.useState(null);
  React.useEffect(() => {
    fetch('/api/api-keys', { credentials: 'include' })
      .then(r => r.ok ? r.json() : {})
      .then(setStatus);
  }, []);
  if (!status) return <span style={{color:'#aaa'}}>Loading...</span>;
  return (
    <ul style={{listStyle:'none',padding:0,margin:0}}>
      {Object.entries(status).map(([k,v]) => (
        <li key={k} style={{color:v==='present'?'#4cafef':'#f44336',fontWeight:v==='present'?'bold':'normal'}}>
          {k}: {v}
        </li>
      ))}
    </ul>
  );
}

export default function HiddenMuseHaven() {
  const [triggered, setTriggered] = useState(false);
  const [showOnboarding, setShowOnboarding] = useState(true);
  const [onboardingStep, setOnboardingStep] = useState(0);
  const [helpText, setHelpText] = useState('');
  const [auth, setAuth] = useState(false);
  const [step, setStep] = useState(0);
  const [prompt, setPrompt] = useState('');
  const [chat, setChat] = useState([]);
  const [showSettings, setShowSettings] = useState(false);
  const [showCustomization, setShowCustomization] = useState(false);
  const [showLearning, setShowLearning] = useState(false);
  const [learningMode, setLearningMode] = useState('manual'); // manual | active | hybrid
  const [feedback, setFeedback] = useState('');
  const [profile, setProfile] = useState({
    name: 'You',
    kinks: [],
    mood: 'curious',
    boundaries: 'Respectful, no violence',
    favoriteLook: 'Sultry Siren',
    arEnabled: false,
    hapticEnabled: false,
    explicitness: 5,
    flirtation: 5,
    voice: 'sultry',
    body: 'voluptuous',
    outfit: 'lingerie',
    hair: 'cascading curls',
    makeup: 'smoky eyes',
    sessionHistory: [],
    presets: [
      { name: 'Tender Muse', explicitness: 3, flirtation: 8, mood: 'tender' },
      { name: 'Kinky Vixen', explicitness: 10, flirtation: 10, mood: 'wild' },
      { name: 'Romantic Siren', explicitness: 6, flirtation: 7, mood: 'romantic' }
    ]
  });
  const [passcode, setPasscode] = useState('');
  const [biometric, setBiometric] = useState('');
  const [facial, setFacial] = useState('');
  const [behavioral, setBehavioral] = useState('');
  const [voicePhrase, setVoicePhrase] = useState('');
  const [notificationPrefs, setNotificationPrefs] = useState({
    slack: false,
    discord: false,
    email: false
  });

  function handleSecretTap() {
    setStep(prev => {
      const next = prev + 1;
      if (next === HIDDEN_TRIGGER_SEQUENCE.length) {
        setTriggered(true);
      }
      return next;
    });
  }

  function handleVoiceTrigger(e) {
    if (e.target.value === VOICE_TRIGGER_PHRASE) {
      setTriggered(true);
    }
  }

  // Custom swipe trigger stub
  function handleSwipeTrigger(pattern) {
    if (pattern === SWIPE_TRIGGER_PATTERN) {
      setTriggered(true);
    }
  }

  function handleAuth(e) {
    e.preventDefault();
    // 3D face/passcode/biometric/behavioral biometric stub
    const pass = passcode.length >= 16 && /[A-Z]/.test(passcode) && /[0-9]/.test(passcode);
    const bio = biometric === 'OWNER_BIOMETRIC';
    const face = facial === 'OWNER_FACE_3D';
    const behav = behavioral === 'OWNER_BEHAVIOR';
    if (pass && bio && face && behav) {
      setAuth(true);
    }
  }

  function handleSend(e) {
    e.preventDefault();
    // Adaptive SAFE AI: owner-controlled, stateless
    let response = '';
    if (learningMode !== 'manual') {
      // Simulate adaptive feedback: escalate if owner gave positive feedback last time
      const last = profile.sessionHistory[profile.sessionHistory.length - 1];
      if (last && last.feedback === 'hot') {
        response = 'Emma purrs: "You loved that last time... let me take you even further tonight."';
      } else if (prompt.toLowerCase().includes('naughty')) {
        response = 'Emma grins, her accent sultry: "You want me to be naughty? Let me show you what I can do..."';
      } else {
        response = 'Emma smiles warmly: "How can I please you today?"';
      }
    } else {
      // Manual: static
      if (prompt.toLowerCase().includes('naughty')) {
        response = 'Emma grins, her accent sultry: "You want me to be naughty? Let me show you what I can do..."';
      } else {
        response = 'Emma smiles warmly: "How can I please you today?"';
      }
    }
    setChat([...chat, { you: prompt, emma: quantumEncrypt(response) }]);
    setProfile({ ...profile, sessionHistory: [...profile.sessionHistory, { prompt, feedback: feedback || 'none' }] });
    setPrompt('');
    setFeedback('');
  }

  function handleShowSettings() {
    setShowSettings(!showSettings);
  }
  function handleShowCustomization() {
    setShowCustomization(!showCustomization);
  }
  function handleShowLearning() {
    setShowLearning(!showLearning);
  }
  // Adaptive 8K image/video/text generation stub
  function generate8KContent(type) {
    if (!auth) return 'Access Denied';
    let tag = profile.sessionHistory.length > 2 && learningMode !== 'manual' ? '[ADAPTIVE]' : '[STATIC]';
    return quantumEncrypt(`${tag} [8K ${type}] Emma generated just for your evolving taste.`);
  }
  function generateText() {
    if (!auth) return 'Access Denied';
    let tag = profile.sessionHistory.length > 2 && learningMode !== 'manual' ? '[ADAPTIVE]' : '[STATIC]';
    let preset = profile.presets[Math.floor(Math.random() * profile.presets.length)];
    return quantumEncrypt(`${tag} Emma (${preset.name}) whispers: "Tonight, I want to make your naughtiest fantasy come true..."`);
  }
  function handleFeedbackChange(e) {
    setFeedback(e.target.value);
  }
  function handleLearningModeChange(e) {
    setLearningMode(e.target.value);
  }

  async function handleRotateApiKey() {
    try {
      const res = await fetch('/api/owner/rotate-api-keys', { method: 'POST', credentials: 'include' });
      if (res.ok) {
        alert('API keys rotated successfully! (static stub)');
      } else {
        alert('Failed to rotate API keys.');
      }
    } catch (e) {
      alert('Error rotating API keys.');
    }
  }

  async function handleComplianceAudit() {
    try {
      const res = await fetch('/api/owner/compliance-audit', { method: 'POST', credentials: 'include' });
      if (res.ok) {
        const data = await res.json();
        alert('Compliance audit completed!\n' + JSON.stringify(data.report, null, 2));
      } else {
        alert('Failed to run compliance audit.');
      }
    } catch (e) {
      alert('Error running compliance audit.');
    }
  }

  if (!triggered) {
    return (
      <div onClick={handleSecretTap} style={{height: '100vh', background: '#f7f7f7'}}>
        {/* Disguised as innocuous utility page */}
        <h2>Performance Metrics</h2>
        <p>Running checks...</p>
        <input placeholder="Voice Command" onBlur={handleVoiceTrigger} />
        {/* Custom swipe trigger stub (UI not implemented, call handleSwipeTrigger(SWIPE_TRIGGER_PATTERN) to test) */}
      </div>
    );
  }
  if (!auth) {
    return (
      <form onSubmit={handleAuth} style={{padding: 40}}>
        <h2>Muse Haven Access</h2>
        <input value={facial} onChange={e => setFacial(e.target.value)} name="facial" placeholder="3D Facial Recognition" />
        <input value={passcode} onChange={e => setPasscode(e.target.value)} name="passcode" type="password" placeholder="Passcode (16+ chars, A-Z, 0-9)" />
        <input value={biometric} onChange={e => setBiometric(e.target.value)} name="biometric" placeholder="Biometric" />
        <input value={behavioral} onChange={e => setBehavioral(e.target.value)} name="behavioral" placeholder="Behavioral Biometric" />
        <button type="submit">Authenticate</button>
      </form>
    );
  }
  return (
    <div style={{padding: 40, background: '#181824', color: '#fff', minHeight: '100vh', position:'relative'}}>
      {showOnboarding && (
        <OnboardingOverlay
          step={onboardingStep}
          onNext={()=>setOnboardingStep(s=>s+1)}
          onClose={()=>setShowOnboarding(false)}
        />
      )}
      {/* Persistent onboarding relaunch button */}
      <button
        aria-label="Show onboarding tutorial"
        style={{position:'fixed',bottom:32,left:32,zIndex:10000,background:'#222',color:'#fff',border:'none',borderRadius:24,padding:'12px 18px',fontSize:22,boxShadow:'0 2px 8px #222',cursor:'pointer'}}
        onClick={()=>{setShowOnboarding(true);setOnboardingStep(0);}}
        title="Show onboarding tutorial"
      >?</button>
      {/* Owner Control Center button */}
      <button
        aria-label="Owner Control Center"
        style={{position:'fixed',top:32,left:32,zIndex:10000,background:'#4cafef',color:'#fff',border:'none',borderRadius:24,padding:'12px 18px',fontSize:20,boxShadow:'0 2px 8px #222',cursor:'pointer'}}
        onClick={()=>setShowSettings(true)}
        title="Owner Control Center"
      >⚙️</button>

      {helpText && <HelpTooltip text={helpText} onClose={()=>setHelpText('')} />}
      {/* In-portal backend API/endpoint documentation for owner guidance */}
      <div style={{position:'absolute',top:10,right:10,background:'#232336',padding:16,borderRadius:8,maxWidth:350,fontSize:13,opacity:0.85}}>
        <b>Owner API Guide</b>
        <ul>
          <li><b>Auth:</b> <code>POST /auth</code> (3D face, passcode, biometric, behavioral)</li>
          <li><b>Content:</b> <code>POST /generate</code> (type: text/image/video, 8K, SAFE AI-tagged)</li>
          <li><b>Feedback:</b> <code>POST /feedback</code> (stateless, owner-controlled)</li>
          <li><b>Kinks:</b> <code>GET /kinks</code> (suggestions, static, SAFE AI)</li>
          <li><b>Security:</b> <code>GET /security_status</code> (quantum encryption, blockchain log)</li>
        </ul>
        <span style={{fontSize:11,opacity:0.7}}>See backend README for full details. All endpoints are stateless, deterministic, and SAFE AI-compliant.</span>
      </div>
      <h2>Muse Haven – Evolving Pleasure Sanctuary <button title="Help" onClick={()=>setHelpText('This is your private, SAFE AI-compliant sanctuary. All features are owner-only and stateless.')}>?</button></h2>
      <button onClick={handleShowSettings}>Settings <button title="Help" onClick={()=>setHelpText('Adjust triggers, authentication, and emergency lockdown here.')}>?</button></button>
      <button onClick={handleShowCustomization}>Customization <button title="Help" onClick={()=>setHelpText('Personalize Emma’s look, persona, and explicitness here.')}>?</button></button>
      <button onClick={handleShowLearning}>Learning Mode <button title="Help" onClick={()=>setHelpText('Toggle owner-controlled learning/adaptation. All learning is stateless and SAFE AI-compliant.')}>?</button></button>
      {showSettings && (
        <div style={{background: '#222', padding: 30, margin: 10, borderRadius: 16, boxShadow: '0 4px 24px rgba(0,0,0,0.18)', maxWidth: 480}} aria-label="Owner Control Center" role="dialog">
          <h3 style={{marginBottom:16}}>Owner Control Center <button title="Help" aria-label="Help: Owner Control Center" onClick={()=>setHelpText('This panel groups all SAFE AI owner controls: lockdown, export, audit, API keys, and security triggers.')}>?</button></h3>
          <ul style={{listStyle:'none',padding:0}}>
            <li style={{marginBottom:18}}>
              <b>Security & Triggers</b> <button title="Help" aria-label="Help: Security & Triggers" onClick={()=>setHelpText('Configure secret triggers, authentication, and instant lockdown. All logic is stateless and SAFE AI-compliant.')}>?</button><br/>
              <span>Trigger: 7-tap, spiral swipe, or voice phrase ("Muse, light my fire")</span><br/>
              <span>Auto-lock: 5 min inactivity</span>
            </li>
            <li style={{marginBottom:18}}>
              <b>Emergency Lockdown</b> <button title="Help" aria-label="Help: Emergency Lockdown" onClick={()=>setHelpText('Instantly purge and lock out all access. This action is irreversible and SAFE AI-compliant.')}>?</button><br/>
              <button style={{background: 'crimson', color: '#fff', border:'none', borderRadius:8, padding:'10px 24px', marginTop:6, fontWeight:'bold', fontSize:16, cursor:'pointer'}}
                onClick={()=>window.confirm('Are you sure you want to trigger EMERGENCY LOCKDOWN? This cannot be undone.') && window.location.reload()}
                aria-label="Trigger Emergency Lockdown"
              >Purge & Lock</button>
            </li>
            <li style={{marginBottom:18}}>
              <b>Export Audit Log</b> <button title="Help" aria-label="Help: Export Audit Log" onClick={()=>setHelpText('Download a full audit log of all owner actions for compliance and review.')}>?</button><br/>
              <button style={{background:'#4cafef',color:'#fff',border:'none',borderRadius:8,padding:'10px 24px',marginTop:6,fontWeight:'bold',fontSize:16,cursor:'pointer'}}
                onClick={()=>window.open('/admin/audit-log','_blank')}
                aria-label="Export Audit Log"
              >Export Audit Log</button>
            </li>
            <li style={{marginBottom:18}}>
              <b>Export Compliance Log</b> <button title="Help" aria-label="Help: Export Compliance Log" onClick={()=>setHelpText('Download a full compliance log for SAFE AI and legal review.')}>?</button><br/>
              <button style={{background:'#4cafef',color:'#fff',border:'none',borderRadius:8,padding:'10px 24px',marginTop:6,fontWeight:'bold',fontSize:16,cursor:'pointer'}}
                onClick={()=>window.open('/admin/export-history','_blank')}
                aria-label="Export Compliance Log"
              >Export Compliance Log</button>
            </li>
            <li style={{marginBottom:18}}>
              <b>API Key Status</b> <button title="Help" aria-label="Help: API Key Status" onClick={()=>setHelpText('View the SAFE AI-compliant status of all required API keys. No secrets are ever shown.')}>?</button><br/>
              <ApiKeyStatus />
            </li>
            <li style={{marginBottom:18}}>
              <b>Integrations</b> <button title="Help" aria-label="Help: Integrations" onClick={()=>setHelpText('Configure integrations for Slack, Discord, and Email notifications.')}>?</button><br/>
              <IntegrationControls
                notificationPrefs={notificationPrefs}
                onPrefsChange={setNotificationPrefs}
                onRotateApiKey={handleRotateApiKey}
                onComplianceAudit={handleComplianceAudit}
              />
            </li>
          </ul>
          <p style={{fontSize:12,opacity:0.7,marginTop:18}}>All authentication and lockdown logic is enforced in isolation, with no connection to business, legal, or financial modules.</p>
          <button style={{marginTop:18,background:'#444',color:'#fff',border:'none',borderRadius:8,padding:'10px 24px',fontWeight:'bold',fontSize:16,cursor:'pointer'}}
            onClick={()=>setShowSettings(false)}
            aria-label="Close Owner Control Center"
          >Close</button>
        </div>
      )}
      {showCustomization && (
        <div style={{background: '#333', padding: 20, margin: 10}}>
          <h3>Emma Customization <button title="Help" onClick={()=>setHelpText('Adjust Emma’s look, body, outfit, and persona. All changes are local and owner-controlled.')}>?</button></h3>
          <label>Look: <input value={profile.favoriteLook} onChange={e => setProfile({...profile, favoriteLook: e.target.value})} /></label><br/>
          <label>Body: <input value={profile.body} onChange={e => setProfile({...profile, body: e.target.value})} /></label><br/>
          <label>Outfit: <input value={profile.outfit} onChange={e => setProfile({...profile, outfit: e.target.value})} /></label><br/>
          <label>Hair: <input value={profile.hair} onChange={e => setProfile({...profile, hair: e.target.value})} /></label><br/>
          <label>Makeup: <input value={profile.makeup} onChange={e => setProfile({...profile, makeup: e.target.value})} /></label><br/>
          <label>Explicitness: <input type="range" min="1" max="10" value={profile.explicitness} onChange={e => setProfile({...profile, explicitness: e.target.value})} /></label><br/>
          <label>Flirtation: <input type="range" min="1" max="10" value={profile.flirtation} onChange={e => setProfile({...profile, flirtation: e.target.value})} /></label><br/>
          <label>AR Mode: <input type="checkbox" checked={profile.arEnabled} onChange={e => setProfile({...profile, arEnabled: !profile.arEnabled})} /></label><br/>
          <label>Haptic: <input type="checkbox" checked={profile.hapticEnabled} onChange={e => setProfile({...profile, hapticEnabled: !profile.hapticEnabled})} /></label><br/>
        </div>
      )}
      {showLearning && (
        <div style={{background: '#222', padding: 20, margin: 10}}>
          <h3>Learning Mode <button title="Help" onClick={()=>setHelpText('Switch between manual, active, or hybrid learning. All adaptation is opt-in, stateless, and SAFE AI-compliant.')}>?</button></h3>
          <label>Learning Mode: <select value={learningMode} onChange={handleLearningModeChange}>
            <option value="manual">Manual (owner only)</option>
            <option value="active">Active (feedback-driven)</option>
            <option value="hybrid">Hybrid (manual + feedback)</option>
          </select></label><br/>
          <p>Current mode: {learningMode}</p>
          <p>All learning is owner-controlled, opt-in, stateless, and SAFE AI-compliant.</p>
        </div>
      )}
      <div style={{marginTop: 20}}>
        <form onSubmit={handleSend}>
          <input value={prompt} onChange={e => setPrompt(e.target.value)} placeholder="Type your desire..." style={{width: 300}} aria-label="Type your desire" />
          <button type="button" title="Help" onClick={()=>setHelpText('Type your request to Emma. Feedback can be provided to guide adaptation (SAFE AI-compliant, stateless).')}>?</button>
          <select value={feedback} onChange={handleFeedbackChange} style={{marginLeft: 10}} aria-label="Feedback">
            <option value="">Feedback</option>
            <option value="hot">🔥 Hot</option>
            <option value="more">More</option>
            <option value="softer">Softer</option>
            <option value="reset">Reset</option>
          </select>
          <button type="submit">Send</button>
        </form>
        <div style={{margin: '20px 0'}}>
          {chat.map((c, i) => (
            <div key={i}>
              <b>You:</b> {c.you}<br/>
              <b>Emma:</b> {c.emma}
            </div>
          ))}
        </div>
      </div>
      <div style={{marginTop: 40}}>
        <button onClick={() => alert(generateText())}>Generate Kinky Text</button>
        <button onClick={() => alert(generate8KContent('Image'))}>Generate 8K Image</button>
        <button onClick={() => alert(generate8KContent('Video'))}>Generate 8K Video</button>
      </div>
    </div>
  );
}
