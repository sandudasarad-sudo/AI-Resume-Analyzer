from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


def generate_pdf_report(
    target_role,
    resume_skills,
    matched_skills,
    missing_skills,
    match_percentage,
    ml_results,
):
    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=45,
        leftMargin=45,
        topMargin=45,
        bottomMargin=45,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        textColor=colors.HexColor("#2563eb"),
        fontSize=22,
        spaceAfter=18,
    )

    story = []

    story.append(
        Paragraph("AI RESUME ANALYSIS REPORT", title_style)
    )

    story.append(
        Paragraph(
            f"<b>Selected Career Role:</b> {target_role}",
            styles["Normal"],
        )
    )

    story.append(Spacer(1, 18))

    story.append(
        Paragraph("1. Analysis Summary", styles["Heading2"])
    )

    summary_data = [
        ["Metric", "Result"],
        ["Detected Technical Skills", str(len(resume_skills))],
        ["Matching Skills", str(len(matched_skills))],
        ["Skills Not Detected", str(len(missing_skills))],
        ["Role Skill Coverage", f"{match_percentage}%"],
    ]

    summary_table = Table(
        summary_data,
        colWidths=[3.5 * inch, 2 * inch],
    )

    summary_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1d4ed8")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("PADDING", (0, 0), (-1, -1), 8),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ])
    )

    story.append(summary_table)
    story.append(Spacer(1, 18))

    def add_skill_section(title, skills):
        story.append(Paragraph(title, styles["Heading2"]))

        if skills:
            story.append(
                Paragraph(
                    ", ".join(skills),
                    styles["BodyText"],
                )
            )
        else:
            story.append(
                Paragraph("None detected.", styles["BodyText"])
            )

        story.append(Spacer(1, 12))

    add_skill_section(
        "2. Detected Technical Skills",
        resume_skills,
    )

    add_skill_section(
        "3. Skills Matching the Selected Role",
        matched_skills,
    )

    add_skill_section(
        "4. Skills Not Detected in the Role Checklist",
        missing_skills,
    )

    story.append(
        Paragraph(
            "5. Job Role Text Similarity",
            styles["Heading2"],
        )
    )

    similarity_data = [["Job Role", "Text Similarity"]]

    for item in ml_results:
        similarity_data.append([
            item["Job Role"],
            f'{item["Text Similarity (%)"]}%',
        ])

    similarity_table = Table(
        similarity_data,
        colWidths=[3.5 * inch, 2 * inch],
        repeatRows=1,
    )

    similarity_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f766e")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("PADDING", (0, 0), (-1, -1), 7),
        ])
    )

    story.append(similarity_table)
    story.append(Spacer(1, 20))

    story.append(
        Paragraph("Important Notes", styles["Heading2"])
    )

    story.append(
        Paragraph(
            "This report uses keyword matching and TF-IDF text similarity. "
            "Text similarity is not a hiring probability or a prediction "
            "of employment. Skills not detected in the PDF may still "
            "be skills the candidate possesses.",
            styles["BodyText"],
        )
    )

    document.build(story)

    buffer.seek(0)
    return buffer.getvalue()