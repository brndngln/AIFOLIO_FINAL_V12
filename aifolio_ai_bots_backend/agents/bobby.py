# backend/agents/bobby.py

from .agent_utils import (
    sanitize_input, moderate_content, log_interaction, raise_if_sentience_attempted,
    static_typo_grammar_check, static_tone_voice_match, calculate_risk_score, static_asset_health_check,
    encrypt_audit_log_entry, notify_slack, notify_discord, notify_email
)
from aifolio_empire.systems_infrastructure.openai_api_simulator import OpenAISimulator

def handle_bobby(user_input: str, user: str = "anonymous") -> str:
    """
    Elite SAFE AI-compliant handler: stateless, deterministic, fully auditable, and owner-controlled.
    Integrates typo/grammar check, tone/voice match, risk scoring, asset health, and encrypted audit logging.
    All extension points are static, non-adaptive, and documented for future SAFE AI integrations.
    """
    safe_input = sanitize_input(user_input)
    # Static typo/grammar check
    grammar_report = static_typo_grammar_check(safe_input)
    # Static tone/voice match
    tone_report = static_tone_voice_match(safe_input, target="professional")
    # Static risk score
    risk_score = calculate_risk_score(safe_input)
    # Static asset health check (example asset)
    asset_health = static_asset_health_check({"input": safe_input})
    # Enhanced compliance: pass user_consent in context
    context = {
        "user_consent": True,
        "grammar": grammar_report,
        "tone": tone_report,
        "risk": risk_score,
        "asset_health": asset_health
    }
    moderation = moderate_content(safe_input)
    if moderation.get("block_reason") or moderation.get("human_review_required"):
        encrypted_log = encrypt_audit_log_entry({
            "agent": "bobby",
            "user": user,
            "input": safe_input,
            "output": f"[BLOCKED: {moderation.get('block_reason','compliance')}]",
            "context": context,
            "SAFE_AI_compliant": True
        })
        # Log encrypted, static notification
        notify_slack({"event": "block", "agent": "bobby", "user": user, "reason": moderation.get('block_reason')})
        with open("ai_bots_audit.log", "a") as f:
            f.write(encrypted_log + "\n")
        return f"Sorry, this request cannot be processed due to compliance or safety policies. [Reason: {moderation.get('block_reason','compliance')}]"
    raise_if_sentience_attempted(safe_input)
    system_prompt = (
        "You are Bobby, a helpful assistant. Your sole task is to offer business advice, strategies, and growth tactics. "
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
        log_interaction("bobby", safe_input, f"[BLOCKED-OUTPUT: {moderation_out.get('block_reason','compliance')}]", moderation_out, user)
        return f"Sorry, the generated response was blocked for compliance or safety reasons. [Reason: {moderation_out.get('block_reason','compliance')}]"
    raise_if_sentience_attempted(output)
    log_interaction("bobby", safe_input, output, moderation_out, user)
    return output
