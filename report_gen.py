from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.platypus.flowables import KeepTogether
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from datetime import datetime

def generate_pdf_report(url, alerts, filepath):
    doc = SimpleDocTemplate(filepath, pagesize=letter,
                            rightMargin=inch/2, leftMargin=inch/2,
                            topMargin=inch, bottomMargin=inch)
    styles = getSampleStyleSheet()
    elements = []

    # Custom styles
    title_style = ParagraphStyle(
        'title',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#0073C8'),  # blue color
        spaceAfter=12,
    )

    subtitle_style = ParagraphStyle(
        'subtitle',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=8,
    )

    normal_style = styles['Normal']
    normal_style.spaceAfter = 6

    # Table cell style with wrapping and smaller font
    cell_style = ParagraphStyle(
        'cell',
        fontSize=8,
        leading=10,
        alignment=TA_LEFT,
    )

    # Header with shield emoji and blue color
    elements.append(Paragraph('🛡 SecureNexus', title_style))
    elements.append(Paragraph('Web Vulnerability Scan Report', subtitle_style))

    # URL and time info
    scan_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    elements.append(Paragraph(f'<b>Scanned URL:</b> {url}', normal_style))
    elements.append(Paragraph(f'<b>Scan Time:</b> {scan_time}', normal_style))

    elements.append(Spacer(1, 12))

    if not alerts:
        elements.append(Paragraph('No alerts found.', normal_style))
    else:
        # Prepare table data
        table_data = []
        # Table headers
        headers = ['Alert', 'Risk', 'Description', 'URL', 'Parameter']
        table_data.append(headers)

        # Populate rows with Paragraphs for wrapping text
        for alert in alerts:
            row = [
                Paragraph(alert.get('alert', 'N/A'), cell_style),
                Paragraph(alert.get('risk', 'N/A'), ParagraphStyle('centered', fontSize=8, alignment=TA_CENTER)),
                Paragraph(alert.get('description', 'N/A').replace('\n', '<br />'), cell_style),
                Paragraph(alert.get('url', 'N/A'), cell_style),
                Paragraph(alert.get('param', 'N/A'), cell_style),
            ]
            table_data.append(row)

        # Create table with fixed column widths (adjust as needed)
        col_widths = [1.5*inch, 0.7*inch, 3*inch, 2*inch, 1*inch]

        table = Table(table_data, colWidths=col_widths, repeatRows=1)
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0073C8')),  # header blue
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('ALIGN', (1, 1), (1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey]),
            ('LEFTPADDING', (0,0), (-1,-1), 4),
            ('RIGHTPADDING', (0,0), (-1,-1), 4),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ])
        table.setStyle(table_style)
        elements.append(table)

    doc.build(elements)
