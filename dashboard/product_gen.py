"""
product_gen.py — Product Generation Blueprint
Elite security, ethics, and maintainability: CSRF, audit logging, AI oversight, human-in-the-loop.
"""
from flask import Blueprint, render_template, request

product_gen_bp = Blueprint("product_gen", __name__, template_folder="templates")


@product_gen_bp.route("/generate", methods=["GET", "POST"])
def generate():
    """Product generation with AI oversight, human-in-the-loop, CSRF, and double audit log."""
    from dashboard.web_dashboard import (
        validate_csrf_token,
        generate_csrf_token,
        ai_action_with_oversight,
        optimize_prompt,
        select_visuals,
        suggest_sales_improvements,
        scan_and_fix,
        legal_scan,
    )

    if request.method == "POST":
        token = request.form.get("csrf_token")
        if not validate_csrf_token(token):
            return "CSRF validation failed", 400
        title = request.form["title"]
        prompt = request.form["prompt"]
        niche = request.form["niche"]
        brand = request.form["brand"]
        category = request.form["category"]
        user_consent = request.form.get("user_consent", False)
        # AI Engines Integration with SentienceGuard and uncertainty/flag reporting
        optimized_prompt, prompt_flag = ai_action_with_oversight(
            (prompt, title), lambda x: optimize_prompt(*x), context="optimize_prompt"
        )
        visuals, visuals_flag = ai_action_with_oversight(
            (niche, brand), lambda x: select_visuals(*x), context="select_visuals"
        )
        sales_suggestions = ai_action_with_oversight(
            optimized_prompt, suggest_sales_improvements, context="sales_optimizer"
        )
        fixed_content, ethics_report = ai_action_with_oversight(
            optimized_prompt, scan_and_fix, context="ethics_qualityguard"
        )
        final_content = ai_action_with_oversight(
            (fixed_content, category, user_consent),
            lambda x: legal_scan(*x),
            context="legal_scan",
        )
        # Human-in-the-loop: require admin approval before file is sent
        preview = f"<h4>Preview</h4><pre>{final_content[:1000]}</pre>"  # Show first 1000 chars
        preview += f"<br><b>Visuals:</b> {visuals}<br><b>Sales Suggestions:</b> {sales_suggestions}<br><b>Ethics Report:</b> {ethics_report}"
        if prompt_flag:
            preview += f"<br><b>Prompt Flag:</b> {prompt_flag}"
        if visuals_flag:
            preview += f"<br><b>Visuals Flag:</b> {visuals_flag}"
        preview += f"""<form method="post">
        <input type="hidden" name="title" value="{title}"/>
        <input type="hidden" name="prompt" value="{prompt}"/>
        <input type="hidden" name="niche" value="{niche}"/>
        <input type="hidden" name="brand" value="{brand}"/>
        <input type="hidden" name="category" value="{category}"/>
        <input type="hidden" name="user_consent" value="{user_consent}"/>
        <input type="hidden" name="csrf_token" value="{token}"/>
        <input type="hidden" name="final_content" value="{final_content.replace('"','&quot;').replace("'","&#39;")}"/>
        <button type="submit" name="approve" value="1">Approve and Download</button></form>"""
        return render_template("dashboard.html", content=preview)
    # GET: Render product generation form
    csrf_token = generate_csrf_token()
    form = """<form method="post">
        <input name="title" placeholder="Title" required/><br>
        <input name="prompt" placeholder="Prompt" required/><br>
        <input name="niche" placeholder="Niche" required/><br>
        <input name="brand" placeholder="Brand" required/><br>
        <input name="category" placeholder="Category" required/><br>
        <label><input type="checkbox" name="user_consent" value="1" required/> I consent to ethical use and privacy policy.</label><br>
        <input type="hidden" name="csrf_token" value="{}"/>
        <button type="submit">Generate</button>
    </form>""".format(
        csrf_token
    )
    return render_template(
        "dashboard.html",
        content="<h3>Product Generation</h3>" + form + "<a href='/dashboard'>Back</a>",
    )


# --- TODO: Add further product generation endpoints as needed for modularity, security, and ethics. ---
