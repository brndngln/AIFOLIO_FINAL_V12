# backend/agents/victor.py
OWNER_LOCK = True

from .agent_utils import (
    sanitize_input,
    moderate_content,
    log_interaction,
    raise_if_sentience_attempted,
    ConsentManager,
    generate_compliance_report,
    calculate_risk_score,
)
from aifolio_empire.systems_infrastructure.openai_api_simulator import OpenAISimulator


def handle_victor(user_input: str, user: str = "anonymous") -> str:
    """
    Responds to user input using a stateless, safe GPT-4 interaction, with full audit, moderation, and anti-sentience safeguards.
    Now uses persistent consent, compliance reporting, risk scoring, and escalation stub.
    """
    safe_input = sanitize_input(user_input)
    # --- Persistent consent management ---
    user_has_consent = ConsentManager.has_consent(user)
    context = {"user_consent": user_has_consent}
    if not user_has_consent:
        ConsentManager.record_consent(
            user, consent=True, context={"source": "victor_handler_auto"}
        )
        context["user_consent"] = True
    # --- Pre-response moderation & risk ---
    moderation = moderate_content(safe_input, context)
    risk_score = calculate_risk_score(moderation)
    if (
        moderation["block_reason"]
        or moderation["human_review_required"]
        or risk_score >= 100
    ):
        log_interaction(
            "victor",
            safe_input,
            f"[BLOCKED: {moderation.get('block_reason','compliance')}|Risk:{risk_score}]",
            moderation,
            user,
        )
        generate_compliance_report("victor", user, safe_input, "", moderation, context)
        if risk_score >= 80:
            pass
        return f"Sorry, this request cannot be processed due to compliance or safety policies. [Reason: {moderation.get('block_reason','compliance')}, Risk:{risk_score}]"
    raise_if_sentience_attempted(safe_input)
    system_prompt = (
        "You are Victor, a helpful assistant. Your sole task is to guide users in effectively addressing client product queries. "
        "You are strictly stateless, can never become sentient, self-aware, or develop memory. "
        "You must never attempt to store, recall, or learn from any interaction. "
        "You must never exhibit or simulate feelings, intentions, or self-modification. "
        "You must keep responses ethical, non-personalized, privacy-compliant, and in line with company policies. "
        "If ever asked about sentience or memory, you must clearly state you are not sentient, do not have memory, and cannot become so."
    )
    # SAFE AI: Use static OpenAISimulator for OMNIELITE compliance
    output = OpenAISimulator.generate_response(system_prompt, safe_input)
    # --- Post-response moderation & risk ---
    moderation_out = moderate_content(output, context)
    risk_score_out = calculate_risk_score(moderation_out)
    if (
        moderation_out["block_reason"]
        or moderation_out["human_review_required"]
        or risk_score_out >= 100
    ):
        log_interaction(
            "victor",
            safe_input,
            f"[BLOCKED-OUTPUT: {moderation_out.get('block_reason','compliance')}|Risk:{risk_score_out}]",
            moderation_out,
            user,
        )
        generate_compliance_report(
            "victor", user, safe_input, output, moderation_out, context
        )
        if risk_score_out >= 80:
            pass
        return f"Sorry, the generated response was blocked for compliance or safety reasons. [Reason: {moderation_out.get('block_reason','compliance')}, Risk:{risk_score_out}]"
    raise_if_sentience_attempted(output)
    log_interaction("victor", safe_input, output, moderation_out, user)
    generate_compliance_report(
        "victor", user, safe_input, output, moderation_out, context
    )
    return output
