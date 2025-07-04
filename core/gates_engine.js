// Gates Engine: Problem-first prompt priority engine
export class GatesEngine {
  prioritizePrompt(promptSet) {
    // Sort prompts by problem impact (stub)
    return promptSet.sort((a, b) => (b.impact || 0) - (a.impact || 0));
  }
}
export default new GatesEngine();
