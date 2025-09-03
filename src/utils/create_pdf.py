from reportlab.lib.pagesizes import LETTER, A4
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import os

def create_non_group_invoice_pdf(nit, client, list_rolls, path_folder):
    os.makedirs(path_folder, exist_ok=True)
    
    # Crear PDF
    filename = os.path.join(path_folder, f"Factura.pdf")
    doc = SimpleDocTemplate(filename, pagesize=LETTER)
    styles = getSampleStyleSheet()
    style_heading = styles["Heading1"]
    style_normal = styles["Normal"]
    elements = []

    # Título
    elements.append(Paragraph("Nota de entrega", style_heading))
    elements.append(Paragraph(f"NIT: {nit}", style_normal))
    elements.append(Spacer(1, 12))

    # Encabezado y datos de tabla
    table_data = [["# Rollo", "Color", "Cantidad (MTS)", "Cantidad (KG)", "Tipo"]]
    for roll in list_rolls:
        table_data.append([
            str(roll["roll"]),
            str(roll["color"]),
            f"{round(roll['mts'], 3)}",
            f"{round(roll['kg'], 3)}",
            str(roll["item"]),
        ])

    table = Table(table_data, colWidths=[80, 150, 100, 100])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(table)
    doc.build(elements)
    print(f"Info: PDF rollo a rollo: {filename} [Completado]")




def create_group_invoice_pdf(client_nit: str, client: str, color_group: dict, path_folder: str, note_number):

    # Crear directorio si no existe
    os.makedirs(path_folder, exist_ok=True)
    
    # Configurar estilos
    styles = getSampleStyleSheet()
    style_normal = styles["Normal"]
    
    # Generar datos dinámicos
    today = datetime.today().strftime("%d/%m/%Y")
    
    
    # Crear archivo PDF
    pdf_filename = os.path.join(path_folder, "Nota de entrega.pdf")
    doc = SimpleDocTemplate(pdf_filename, pagesize=A4)
    elements = []
    
    # ---- Encabezado empresa (izquierda) ----
    company_info = [
        ["Aurumtex S.A.S"],
        ["NIT: 901.698.558-1"],
        ["CLL 19 # 69-86"],
        ["TEL: (691)7047422"],
        ["BOGOTÁ - COLOMBIA"],
        ["contabilidad@aurumtex.com"]
    ]
    company_table = Table(company_info, colWidths=[200])
    company_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 1),      # Reducir padding superior
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1),   # Reducir padding inferior
    ]))
    
    # ---- Info Nota de Entrega (derecha) - Sin bordes ----
    delivery_basic_info = [
        ["NOTA DE ENTREGA:", note_number],
        ["FECHA:", today],
        ["ITC:", ""]
    ]
    delivery_basic_table = Table(delivery_basic_info, colWidths=[150, 100])
    delivery_basic_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 1),      # Reducir padding superior
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1),   # Reducir padding inferior
        ("LINEBELOW", (0, 1), (1, 1), 0.5, colors.black),  # Línea debajo de FECHA
        # SIN BORDES - solo texto con línea bajo fecha
    ]))
    
    # ---- Tabla con texto informativo (solo borde exterior, sin líneas internas) ----
    info_text = [
        ["ESTE DOCUMENTO NO VA CON PRECIOS"],
        ["VAN EN LA FACTURA ELECTRÓNICA"],
        ["APLICA LAS NORMAS RELATIVAS"]
    ]
    info_table = Table(info_text, colWidths=[250])
    info_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 2),     # Reducir padding superior
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),  # Reducir padding inferior
        # Solo bordes exteriores
        ("BOX", (0, 0), (-1, -1), 0.5, colors.black),  # Solo el borde exterior
    ]))
    
    # Combinar delivery_basic_table e info_table verticalmente
    delivery_section = Table([
        [delivery_basic_table],
        [Spacer(1, 10)],
        [info_table]
    ], colWidths=[250])
    delivery_section.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    
    # ---- Combinar en una tabla principal (dos columnas) ----
    header_table = Table(
        [[company_table, delivery_section]],
        colWidths=[250, 300]
    )
    header_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    
    elements.append(header_table)
    elements.append(Spacer(1, 20))
    
    # ---- Tabla de productos ----
    headers = ["REFERENCIA", "TOTAL PIEZAS", "MTR", "OBSERVACIONES"]
    table_data = [headers]
    
    # Agregar datos del color_group
    for item in color_group:
        for color, info_color in color_group[item].items():
            row = [
                color,  # REFERENCIA (color)
                int(info_color.get("count_rolls", 0)),  # TOTAL PIEZAS
                round(info_color.get("mts", 0), 2),     # MTR
                info_color.get("container", ""),        # OBSERVACIONES
            ]
            table_data.append(row)
    
    # Agregar filas vacías si hay pocas entradas para mantener el diseño
    while len(table_data) < 7:  # Mínimo 6 filas de datos + 1 header
        table_data.append(["", "", "", ""])
    
    # Crear tabla con anchos ajustados
    table = Table(table_data, colWidths=[120, 100, 80, 150])
    table.setStyle(TableStyle([
        # Encabezados
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("TOPPADDING", (0, 0), (-1, 0), 8),
        ("TOPPADDING", (0, 1), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 6),
        
        # Bordes
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
    ]))
    
    elements.append(table)
    elements.append(Spacer(1, 20))
    
    # Generar el PDF
    doc.build(elements)
    print(f"Info: PDF nota de entrega: {pdf_filename} [Completado]")

