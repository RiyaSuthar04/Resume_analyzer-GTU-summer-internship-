from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from datetime import datetime

def generate_pdf_report(output_path, job_title, candidate_name, results_dict, overall_score):
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    x = 1 * inch
    y = height - 1 * inch

    c.setFont("Helvetica-Bold", 16)
    c.drawString(x, y, "ATS Resume Analysis Report")

    y -= 0.5 * inch
    c.setFont("Helvetica", 12)
    c.drawString(x, y, f"Candidate Name: {candidate_name}")
    y -= 0.3 * inch
    c.drawString(x, y, f"Job Title: {job_title}")
    y -= 0.3 * inch
    c.drawString(x, y, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    y -= 0.5 * inch
    c.setFont("Helvetica-Bold", 14)
    c.drawString(x, y, "Section Scores and Feedback:")

    c.setFont("Helvetica", 11)
    for section, result in results_dict.items():
        y -= 0.4 * inch
        if y < 1.5 * inch:
            c.showPage()
            y = height - 1 * inch
        c.drawString(x, y, f"{section.capitalize()} Score: {result['score']} / 10")
        y -= 0.25 * inch
        c.drawString(x + 0.2 * inch, y, f"Feedback: {result['feedback'][:100]}...")

    y -= 0.6 * inch
    c.setFont("Helvetica-Bold", 12)
    c.drawString(x, y, f"Overall Score: {overall_score:.2f} / 10")

    c.save()
