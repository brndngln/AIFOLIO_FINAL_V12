def generate_growth_strategy(
    title, current_revenue, target_revenue, timeframe, tone="expert"
):
    return f"""
Act as a 7-figure info-product strategist.
Given this product: {title}
Its current revenue is: ${current_revenue}
Goal: Scale to ${target_revenue} within {timeframe}

Build a growth roadmap including:
- TOF / MOF / BOF funnel structure
- Paid + organic content strategy using tone: {tone}
- Weekly KPIs to track (sales, clicks, funnel step conversions)

Format: Step-by-step strategic guide.
"""
