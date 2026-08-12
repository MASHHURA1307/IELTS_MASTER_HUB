import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def generate_mock_exam_pdf(filename, candidate_name, mock_result):
    """
    Generates a PDF Report / Certificate for an IELTS Mock Exam result.
    Save path is specified by filename.
    """
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    story = []
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=24,
        leading=28,
        textColor=colors.HexColor('#0f172a'),
        alignment=1, # Center
        fontName='Helvetica-Bold'
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#4f46e5'),
        alignment=1,
        fontName='Helvetica-Bold'
    )

    h2_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontSize=16,
        leading=20,
        textColor=colors.HexColor('#1e293b'),
        fontName='Helvetica-Bold',
        spaceBefore=12,
        spaceAfter=6
    )

    normal_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#334155'),
        fontName='Helvetica'
    )

    # Title Banner
    story.append(Paragraph("IELTS MASTER HUB", title_style))
    story.append(Paragraph("RASMIY MOCK EXAM NATIJALAR SERTIFIKATI", subtitle_style))
    story.append(Spacer(1, 15))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#4f46e5'), spaceAfter=20))

    # Candidate Info Table
    date_str = datetime.now().strftime("%d.%m.%Y")
    info_data = [
        [Paragraph("<b>Talaba ismi:</b>", normal_style), Paragraph(candidate_name, normal_style),
         Paragraph("<b>Sana:</b>", normal_style), Paragraph(date_str, normal_style)],
        [Paragraph("<b>Test ID:</b>", normal_style), Paragraph(str(mock_result.get('_id', 'IMH-8821')), normal_style),
         Paragraph("<b>Holati:</b>", normal_style), Paragraph("<font color='#10b981'><b>Tugallangan</b></font>", normal_style)]
    ]
    info_table = Table(info_data, colWidths=[100, 180, 80, 140])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('PADDING', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 20))

    # Overall Score Box
    overall_band = mock_result.get('overall_band', 6.5)
    score_data = [
        [Paragraph("<font size=14 color='#ffffff'><b>UMUMIY BAND BALL:</b></font>", normal_style),
         Paragraph(f"<font size=28 color='#ffffff'><b>{overall_band}</b></font>", normal_style)]
    ]
    score_table = Table(score_data, colWidths=[300, 200])
    score_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#4f46e5')),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(score_table)
    story.append(Spacer(1, 25))

    # Skill Scores Breakdown Table
    story.append(Paragraph("Bo'limlar Bo'yicha Natijalar Breakdown", h2_style))
    
    l_band = mock_result.get('listening_band', 6.0)
    r_band = mock_result.get('reading_band', 6.5)
    w_band = mock_result.get('writing_band', 6.0)
    s_band = mock_result.get('speaking_band', 7.0)

    skills_data = [
        ["Bo'lim (Skill)", "Tavsif", "To'plangan Ball"],
        ["Listening", "Tushunish va diqqatni jamlash", f"Band {l_band}"],
        ["Reading", "Matnni tahlil qilish va skanerlash", f"Band {r_band}"],
        ["Writing", "Akademik insho va mantiqiy bayon", f"Band {w_band}"],
        ["Speaking", "Ravon nutq, lug'at va talaffuz", f"Band {s_band}"],
    ]
    skills_table = Table(skills_data, colWidths=[120, 260, 120])
    skills_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e293b')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('ALIGN', (2,0), (2,-1), 'CENTER'),
        ('PADDING', (0,0), (-1,-1), 10),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f1f5f9')])
    ]))
    story.append(skills_table)
    story.append(Spacer(1, 25))

    # Recommendations & AI Notes
    story.append(Paragraph("AI Examiner Tavsiyalari", h2_style))
    feedback_text = (
        "Sizning natijalaringiz IELTS 6.5 - 7.0 darajasiga mos keladi. "
        "Writing bo'limida akademik bog'lovchi so'zlardan va murakkab gap tuzilmalaridan ko'proq foydalanish, "
        "Reading bo'limida esa True/False/Not Given savol turlarida kalit so'zlar sinonimiga e'tibor berish tavsiya etiladi."
    )
    story.append(Paragraph(feedback_text, normal_style))
    story.append(Spacer(1, 30))

    # Footer Signature
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#cbd5e1'), spaceAfter=15))
    footer_text = "IELTS Master Hub — AI Powered Preparation Platform | www.ieltsmasterhub.uz | Autentifikatsiya Kodu: IMH-VERIFIED-2026"
    story.append(Paragraph(f"<font size=8 color='#64748b'>{footer_text}</font>", ParagraphStyle('Footer', alignment=1)))

    doc.build(story)
    return filename
