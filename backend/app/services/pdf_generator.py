from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.pagesizes import A4
from datetime import datetime
from io import BytesIO
import base64
import os
def generate_pdf_base64(profil: str, summary: str, transcript: str, sentiment: str = None) -> str:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []
    # 🔍 Chemin absolu vers le logo depuis ce script
    logo_path = os.path.join(os.path.dirname(__file__), "..", "assets", "logo.jpg")
    logo_path = os.path.abspath(logo_path)
    if os.path.exists(logo_path):
        logo = Image(logo_path, width=1.2*inch, height=1.2*inch)
    else:
        logo = Paragraph("SmartPro", getSampleStyleSheet()["Title"])

    title = Paragraph(f"<b>SmartPro Assistant – Fiche {profil}</b>", styles["Title"])

    # Organise logo + titre dans une table à 2 colonnes
    table_data = [[logo, title]]
    table = Table(table_data, colWidths=[1.5*inch, 5.5*inch])
    table.setStyle(TableStyle([
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('LEFTPADDING', (0, 0), (-1, -1), 0),
    ('RIGHTPADDING', (0, 0), (-1, -1), 0)
]))

    elements.append(table)
    elements.append(Spacer(1, 12))
    now = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    elements.append(Paragraph(f"📅 Date : {now}", styles["Normal"]))
    elements.append(Spacer(1, 12))

    if sentiment:
        elements.append(Paragraph("<b>Analyse de sentiment :</b>", styles["Heading2"]))
        elements.append(Paragraph(sentiment, styles["Normal"]))
        elements.append(Spacer(1, 12))

    # Résumé structuré (découpé par titres)
    elements.append(Paragraph("<b>📄 Compte-rendu structuré :</b>", styles["Heading2"]))
    icon_map = {
        "1.": "🎯 Objectif de l’échange",
        "2.": "📝 Résumé de la discussion",
        "3.": "📌 Points clés / besoins exprimés",
        "4.": "✅ Solutions ou recommandations",
        "5.": "📍 Prochaines étapes"
    }
    # Découpe le résumé en lignes
    current_section = None
    section_content = []

    for line in summary.split("\n"):
        line = line.strip()
        if not line:
            continue  # ignore lignes vides

        # Vérifie si la ligne est un titre de section
        is_section = False
        for key, icon_title in icon_map.items():
            if line.startswith(key):
                # Si on change de section, ajoute le contenu de la section précédente
                if current_section and section_content:
                    elements.append(Spacer(1, 6))
                    for content_line in section_content:
                        elements.append(Paragraph(content_line, styles["Normal"]))
                    section_content = []

                # Ajoute le titre de section
                elements.append(Spacer(1, 8))
                elements.append(Paragraph(f"<b>{icon_title}</b>", styles["Heading3"]))
                current_section = key
                is_section = True
                break

        if not is_section:
            section_content.append(line)

    # Ajoute le contenu de la dernière section
    if section_content:
        elements.append(Spacer(1, 6))
        for content_line in section_content:
            elements.append(Paragraph(content_line, styles["Normal"]))


    elements.append(Spacer(1, 12))
    elements.append(Paragraph("📢 <b>Transcription complète :</b>", styles["Heading2"]))
    elements.append(Paragraph(transcript, styles["Normal"]))

    doc.build(elements)
    pdf_bytes = buffer.getvalue()
    buffer.close()

    return base64.b64encode(pdf_bytes).decode("utf-8")