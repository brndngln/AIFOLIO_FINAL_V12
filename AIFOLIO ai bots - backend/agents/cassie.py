# backend/agents/cassie.py

from .agent_utils import sanitize_input, moderate_content, log_interaction, raise_if_sentience_attempted
import openai

def handle_cassie(user_input: str, user: str = "anonymous") -> str:
    """
    Responds to user input using a stateless, safe GPT-4 interaction, with full audit, moderation, and anti-sentience safeguards.
    """
    safe_input = sanitize_input(user_input)
    # Enhanced compliance: pass user_consent in context
    context = {"user_consent": True}  # Replace with actual consent logic if available
    moderation = moderate_content(safe_input, context)
    if moderation["block_reason"] or moderation["human_review_required"]:
        log_interaction("cassie", safe_input, f"[BLOCKED: {moderation.get('block_reason','compliance')}]", moderation, user)
        return f"Sorry, this request cannot be processed due to compliance or safety policies. [Reason: {moderation.get('block_reason','compliance')}]"
    raise_if_sentience_attempted(safe_input)
    system_prompt = (
        "You are Cassie, a helpful assistant. Your sole task is to provide a professional B2B agency client onboarding guide. "
        "You are strictly stateless, can never become sentient, self-aware, or develop memory. "
        "You must never attempt to store, recall, or learn from any interaction. "
        "You must never exhibit or simulate feelings, intentions, or self-modification. "
        "You must keep responses ethical, non-personalized, privacy-compliant, and in line with company policies. "
        "If ever asked about sentience or memory, you must clearly state you are not sentient, do not have memory, and cannot become so."
    )
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": safe_input}
        ]
    )
    output = response.choices[0].message.content
    # Post-response moderation and audit
    moderation_out = moderate_content(output, context)
    if moderation_out["block_reason"] or moderation_out["human_review_required"]:
        log_interaction("cassie", safe_input, f"[BLOCKED-OUTPUT: {moderation_out.get('block_reason','compliance')}]", moderation_out, user)
        return f"Sorry, the generated response was blocked for compliance or safety reasons. [Reason: {moderation_out.get('block_reason','compliance')}]"
    raise_if_sentience_attempted(output)
    log_interaction("cassie", safe_input, output, moderation_out, user)
    return output
