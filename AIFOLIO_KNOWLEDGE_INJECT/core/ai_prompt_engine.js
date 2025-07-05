// OMNIELITE AI Prompt Engine
// Shared, SAFE AI-compliant logic for all vaults
import { loadPromptSet, applySafetyFilters, sessionMemory } from './prompt_executor.js';

export default class AIFolioPromptEngine {
  constructor(vaultId) {
    this.vaultId = vaultId;
    this.promptSet = loadPromptSet(vaultId);
    this.memory = sessionMemory();
  }
  async generatePrompt(promptId, userInput) {
    const promptTemplate = this.promptSet.find(p => p.id === promptId);
    if (!promptTemplate) throw new Error('Prompt not found');
    let prompt = promptTemplate.prompt.replace(/\{([^}]+)\}/g, (_, k) => userInput[k] || '');
    prompt = applySafetyFilters(prompt, this.vaultId);
    return { prompt, style: promptTemplate.style, title: promptTemplate.title };
  }
}
