from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from datetime import datetime

def generate_pdf_report(url, alerts, output_path):
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()

    # Title style
    title_style = ParagraphStyle(
        'title',
        parent=styles['Heading1'],
        alignment=TA_CENTER,
        fontSize=26,
        spaceAfter=20,
        textColor=colors.HexColor('#004080')  # Dark blue
    )

    # Subtitle style
    subtitle_style = ParagraphStyle(
        'subtitle',
        parent=styles['Heading2'],
        alignment=TA_CENTER,
        fontSize=14,
        spaceAfter=30,
        textColor=colors.HexColor('#0073e6')  # Lighter blue
    )

    # Normal text style
    normal_style = styles['BodyText']

    story = []
    story.append(Paragraph("🛡 SecureNexus", title_style))
    story.append(Paragraph("Web Vulnerability Scan Report", subtitle_style))
    story.append(Paragraph(f"<b>Scanned URL:</b> {url}", normal_style))
    story.append(Paragraph(f"<b>Scan Time:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", normal_style))
    story.append(Spacer(1, 20))

    if not alerts:
        story.append(Paragraph("No vulnerabilities detected.", normal_style))
    else:
        # Prepare table data with headers
        data = [["Alert Name", "Risk Level", "Description", "URL"]]

        for alert in alerts:
            alert_name = alert.get('alert', 'N/A')
            risk = alert.get('risk', 'N/A')
            desc = alert.get('description', 'N/A')
            alert_url = alert.get('uri', 'N/A')

            # Trim description length for neatness
            if len(desc) > 150:
                desc = desc[:147] + "..."

            data.append([alert_name, risk, desc, alert_url])

        # Create the table
        table = Table(data, colWidths=[120, 60, 250, 100])
        # Table style with color-coded risk levels
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#004080')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ])

        # Apply color for risk levels
        risk_color_map = {
            'High': colors.HexColor('#e74c3c'),     # red
            'Medium': colors.HexColor('#f39c12'),   # orange
            'Low': colors.HexColor('#27ae60'),      # green
            'Informational': colors.HexColor('#2980b9')  # blue
        }

        # Color the risk level column per row
        for i, row in enumerate(data[1:], start=1):
            risk_level = row[1]
            color = risk_color_map.get(risk_level, colors.black)
            style.add('TEXTCOLOR', (1, i), (1, i), color)

        table.setStyle(style)
        story.append(table)

    doc.build(story)
