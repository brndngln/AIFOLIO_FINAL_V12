"""
Automated accessibility testing and reporting for AIFOLIO™ dashboard (WCAG 2.1 AA).
Uses axe-core via Selenium for frontend testing.
"""
import json
from selenium import webdriver
from axe_selenium_python import Axe


def run_accessibility_audit(url="http://localhost:8765"):
    # Start headless browser
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    axe = Axe(driver)
    axe.inject()
    results = axe.run()
    driver.quit()
    # Save results
    report_path = "../analytics/accessibility_report.json"
    with open(report_path, "w") as f:
        json.dump(results, f, indent=2)
    return report_path, results


def summarize_accessibility_report(
    report_path="../analytics/accessibility_report.json",
):
    with open(report_path) as f:
        results = json.load(f)
    violations = results.get("violations", [])
    summary = f"Accessibility Violations: {len(violations)}\n"
    by_type = {}
    for v in violations:
        impact = v["impact"]
        by_type[impact] = by_type.get(impact, 0) + 1
        summary += f"- {v['help']} (impact: {impact})\n"
        for node in v["nodes"]:
            summary += f"  On: {node['html']}\n"
    summary += "\nSummary by impact level:\n"
    for impact, count in by_type.items():
        summary += f"- {impact}: {count}\n"
    return summary


def export_accessibility_pdf(report_path="../analytics/accessibility_report.json"):
    from reportlab.pdfgen import canvas
    import io

    with open(report_path) as f:
        results = json.load(f)
    buf = io.BytesIO()
    c = canvas.Canvas(buf)
    y = 800
    c.drawString(30, y, "AIFOLIO Accessibility Report")
    y -= 20
    for v in results.get("violations", []):
        c.drawString(30, y, f"{v['help']} (impact: {v['impact']})")
        y -= 15
        for node in v["nodes"]:
            c.drawString(50, y, f"On: {node['html']}")
            y -= 12
        if y < 50:
            c.showPage()
            y = 800
    c.save()
    buf.seek(0)
    with open("../analytics/accessibility_report.log", "a") as logf:
        logf.write("EXPORT: Accessibility PDF exported\n")
    return buf


def export_accessibility_csv(report_path="../analytics/accessibility_report.json"):
    import io
    import csv

    with open(report_path) as f:
        results = json.load(f)
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Help", "Impact", "HTML"])
    for v in results.get("violations", []):
        for node in v["nodes"]:
            writer.writerow([v["help"], v["impact"], node["html"]])
    with open("../analytics/accessibility_report.log", "a") as logf:
        logf.write("EXPORT: Accessibility CSV exported\n")
    return output.getvalue()


def run_accessibility_audit_on_route(route_url):
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = webdriver.Chrome(options=options)
    driver.get(route_url)
    axe = Axe(driver)
    axe.inject()
    results = axe.run()
    driver.quit()
    report_path = "../analytics/accessibility_report.json"
    with open(report_path, "w") as f:
        json.dump(results, f, indent=2)
    return report_path, results
