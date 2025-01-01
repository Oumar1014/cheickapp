from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from datetime import datetime

class PDFGenerator:
    @staticmethod
    def generate_sales_report(date: datetime, sales_data: list) -> str:
        filename = f"rapport_ventes_{date.strftime('%Y%m%d')}.pdf"
        c = canvas.Canvas(filename, pagesize=A4)
        
        # En-tête
        c.setFont("Helvetica-Bold", 16)
        c.drawString(6*cm, 28*cm, "GESTION DES MOTOS")
        
        c.setFont("Helvetica-Bold", 14)
        c.drawString(6*cm, 27*cm, "NOUHOU BAMMA TOURE")
        
        c.setFont("Helvetica", 12)
        c.drawString(6*cm, 26.5*cm, "Vendeur des motos")
        c.drawString(6*cm, 26*cm, "Tél : +223 77873789 / 90434307 / 83211674")
        c.drawString(6*cm, 25.5*cm, "Adresse : 5eme Quartier GAO Rep.Du Mali")
        
        c.setFont("Helvetica-Bold", 12)
        c.drawString(2*cm, 24*cm, "RAPPORT DES VENTES")
        c.drawString(2*cm, 23.5*cm, f"Date: {date.strftime('%d/%m/%Y')}")
        
        # Tableau
        def draw_table_header(y):
            headers = ['Date', 'Moto', 'Client', 'Quantité', 'Prix unitaire', 'Total']
            x_positions = [2*cm, 4*cm, 8*cm, 12*cm, 14*cm, 16*cm]
            
            # Fond gris pour l'en-tête
            c.setFillColor(colors.lightgrey)
            c.rect(2*cm, y-0.5*cm, 17*cm, 0.8*cm, fill=True)
            c.setFillColor(colors.black)
            
            # Texte de l'en-tête
            c.setFont("Helvetica-Bold", 10)
            for header, x in zip(headers, x_positions):
                c.drawString(x, y, header)
            
            return y - 1*cm
        
        y = draw_table_header(22*cm)
        total_general = 0
        
        # Contenu du tableau
        c.setFont("Helvetica", 10)
        for sale in sales_data:
            if y < 4*cm:  # Nouvelle page
                c.showPage()
                c.setFont("Helvetica-Bold", 12)
                c.drawString(2*cm, 28*cm, "RAPPORT DES VENTES (suite)")
                y = draw_table_header(26*cm)
                c.setFont("Helvetica", 10)
            
            c.drawString(2*cm, y, sale['date'])
            c.drawString(4*cm, y, sale['motorcycle'])
            c.drawString(8*cm, y, sale['client'])
            c.drawString(12*cm, y, str(sale['quantity']))
            c.drawString(14*cm, y, f"{sale['price']:,.0f}")
            c.drawString(16*cm, y, f"{sale['total']:,.0f}")
            
            total_general += sale['total']
            y -= 0.8*cm
        
        # Total général
        y -= 1*cm
        c.setFont("Helvetica-Bold", 11)
        c.drawString(12*cm, y, "TOTAL GÉNÉRAL:")
        c.drawString(16*cm, y, f"{total_general:,.0f} FCFA")
        
        c.save()
        return filename