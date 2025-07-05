"""
AIFOLIO Static HTML Export
Static, deterministic, SAFE AI-compliant static HTML export for sensitive views (no dynamic JS).
"""
import logging

logger = logging.getLogger(__name__)

STATIC_HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AIFOLIO Secure Export</title>
  <link rel="stylesheet" href="/static/style.css">
</head>
<body>
  <div class="secure-content">
    <h1>Secure Export</h1>
    <p>All content is statically rendered. No dynamic JS is present.</p>
  </div>
</body>
</html>
"""


def export_static_html() -> str:
    logger.info("Exported static HTML for sensitive view.")
    return STATIC_HTML_TEMPLATE
