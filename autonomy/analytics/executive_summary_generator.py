"""
AIFOLIO SAFE AI Executive Summary Generator
- Static PDF summary for admins (no rewriting, no optimization)
"""


def generate_executive_summary(stats, output_path):
    # Stub: Write summary to PDF using static template
    with open(output_path, "w") as f:
        f.write("AIFOLIO Executive Summary\n")
        for k, v in stats.items():
            f.write(f"{k}: {v}\n")
    return output_path
