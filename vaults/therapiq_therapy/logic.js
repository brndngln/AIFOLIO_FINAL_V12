// THERAPIQ™ Vault Logic: AI Therapy Style Generator
import AIFolioPromptEngine from '../../core/ai_prompt_engine.js';
import { buildPDF } from '../../core/pdf_builder.js';
import { generateCover } from '../../core/image_generator.js';
import { logEvent } from '../../core/analytics_engine.js';

export async function generateTherapyKit(userInput) {
  const engine = new AIFolioPromptEngine('therapiq_therapy');
  const { prompt, style, title } = await engine.generatePrompt('cbt_framework', userInput);
  // ...AI call or static logic here...
  const content = { title, body: 'Generated therapy plan for ' + userInput.user_goal, coverImg: generateCover('therapiq_therapy', style) };
  const pdf = buildPDF({ content, vaultId: 'therapiq_therapy', style });
  logEvent('therapiq_therapy', 'drop', { userInput });
  return pdf;
}
