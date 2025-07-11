# WIND_PLACEHOLDER
def generate_pdf(content_blocks, metadata):
    from fpdf import FPDF

    pdf = FPDF()
    pdf.add_page()
    for block in content_blocks:
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, block)
    pdf.output(metadata["filename"])
    return metadata["filename"]
