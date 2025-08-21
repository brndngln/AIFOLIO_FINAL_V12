# Consider adding metrics collection for performance monitoring
# Consider using map/filter/reduce for functional style
# Promote pure functions without side effects
import functools
data = {}  # TODO: Define data

def generate_pdf(content_blocks, metadata):
from fpdf import FPDF

  pdf = FPDF()
  pdf.add_page()
  for block in content_blocks:
  pdf.set_font("Arial", size=12)
  pdf.multi_cell(0, 10, block)
  pdf.output(metadata["filename"])
  return metadata["filename"]
