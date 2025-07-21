// OMNIELITE AIFOLIO™ Prompt Executor (Unified for 25 Vaults)
// CommonJS for compatibility with ai_engine.js
const { getVaultPromptSet } = require("../config/prompt_sets/utils.js");

function loadPromptSet(vaultId) {
  return getVaultPromptSet(vaultId);
}

function applySafetyFilters(prompt, vaultId) {
  // Global ethical/safety filters
  let safePrompt = prompt.replace(
    /(password|ssn|credit card|private|personal|address|phone|social security|reflective|memory)/gi,
    "[REDACTED]",
  );
  // Vault-specific tone/filters
  const vaultTones = {
    therapiq: "\n[Tone: Calm, Clinical]",
    ritualux: "\n[Tone: Mystical, Spiritual]",
    rebelremedy: "\n[Tone: Wellness, Natural]",
    loreloom: "\n[Tone: Storybook, Imaginative]",
    ai_mentor: "\n[Tone: Motivational, Youthful]",
    grantgenius: "\n[Tone: Formal, Grant]",
    legalite: "\n[Tone: Legal, Formal]",
    brandcast: "\n[Tone: Personal, Branding]",
    launchloom: "\n[Tone: Ambitious, Launch]",
    coachcraft: "\n[Tone: Coaching, Uplifting]",
    finsmart: "\n[Tone: Financial, Precise]",
    safesignal: "\n[Tone: Crisis, Reassuring]",
    wisdomvault: "\n[Tone: Reflective, Wise]",
    petplan: "\n[Tone: Caring, Informative]",
    cryptomind: "\n[Tone: Educational, Crypto]",
    inventia: "\n[Tone: Innovative, Startup]",
    dealdrip: "\n[Tone: Sales, Persuasive]",
    policygen: "\n[Tone: Policy, Corporate]",
    carechart: "\n[Tone: Health, Supportive]",
    hustlemap: "\n[Tone: Entrepreneurial, Energetic]",
    aiarchive: "\n[Tone: Resourceful, Archival]",
  };
  if (vaultTones[vaultId]) safePrompt += vaultTones[vaultId];
  return safePrompt;
}

function execute({ vaultId, prompt, format, options }) {
  // Load prompt set and apply safety filters
  const promptSet = loadPromptSet(vaultId);
  const safePrompt = applySafetyFilters(prompt, vaultId);
  // Apply format-aware rendering (checklists, stories, SOPs, contracts, journals)
  let rendered;
  switch (format) {
    case "checklist":
      rendered = `Checklist:\n- ` + safePrompt.split("\n").join("\n- ");
      break;
    case "story":
      rendered = `Story:\n${safePrompt}`;
      break;
    case "sop":
      rendered = `Standard Operating Procedure:\n${safePrompt}`;
      break;
    case "contract":
      rendered = `Contract:\n${safePrompt}`;
      break;
    case "journal":
      rendered = `Journal Entry:\n${safePrompt}`;
      break;
    default:
      rendered = safePrompt;
  }
  return rendered;
}

function sessionMemory() {
  // Returns a session-local memory object (no persistence)
  return {};
}

module.exports = {
  loadPromptSet,
  applySafetyFilters,
  execute,
  sessionMemory,
};
