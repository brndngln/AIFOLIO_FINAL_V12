// OMNIELITE AIFOLIO™ AI Engine (Shared Core)
// Unified, ethical, non-sentient, infinitely scalable, owner-controlled

const promptExecutor = require('./prompt_executor');
const styleTuner = require('./style_tuner');
const pdfBuilder = require('./pdf_builder');
const scheduler = require('./scheduler');

function runPrompt({ vaultId, prompt, format, options }) {
  // Ethical limiter and static filter
  if (typeof prompt !== 'string' || prompt.length > 5000) throw new Error('Prompt too long or invalid');
  if (/password|ssn|credit card/i.test(prompt)) throw new Error('Sensitive data not allowed');
  // Style tuning
  const tunedPrompt = styleTuner.tune(prompt, options?.tone || 'default');
  // Execute prompt
  const output = promptExecutor.execute({ vaultId, prompt: tunedPrompt, format, options });
  // Export logic
  if (format === 'pdf') return pdfBuilder.buildPDF(output, options);
  if (format === 'png') return pdfBuilder.buildPNG(output, options);
  if (format === 'zip') return pdfBuilder.buildZIP(output, options);
  return output;
}

module.exports = { runPrompt };
