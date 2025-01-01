from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from datetime import datetime

class InvoiceGenerator:
    @staticmethod
    def generate_invoice(sale_data: dict) -> str:
        filename = f"facture_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
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
        
        # Numéro et date de facture
        c.setFont("Helvetica-Bold", 12)
        c.drawString(2*cm, 24*cm, f"FACTURE N° {datetime.now().strftime('%Y%m%d%H%M')}")
        c.drawString(2*cm, 23.5*cm, f"Date: {datetime.now().strftime('%d/%m/%Y')}")
        
        # Informations client
        c.setFont("Helvetica-Bold", 12)
        c.drawString(2*cm, 22*cm, "CLIENT:")
        c.setFont("Helvetica", 11)
        c.drawString(2*cm, 21.5*cm, f"Nom: {sale_data['client_name']}")
        c.drawString(2*cm, 21*cm, f"Adresse: {sale_data['client_address']}")
        c.drawString(2*cm, 20.5*cm, f"Téléphone: {sale_data['client_phone']}")
        
        # Tableau des produits
        def draw_table_header(y):
            headers = ['Description', 'Quantité', 'Prix unitaire', 'Montant']
            x_positions = [2*cm, 8*cm, 12*cm, 16*cm]
            
            # Fond gris pour l'en-tête
            c.setFillColor(colors.lightgrey)
            c.rect(2*cm, y-0.5*cm, 17*cm, 0.8*cm, fill=True)
            c.setFillColor(colors.black)
            
            # Texte de l'en-tête
            c.setFont("Helvetica-Bold", 11)
            for header, x in zip(headers, x_positions):
                c.drawString(x, y, header)
            
            return y - 1*cm
        
        y = draw_table_header(19*cm)
        
        # Données du produit
        c.setFont("Helvetica", 11)
        c.drawString(2*cm, y, sale_data['name'])
        c.drawString(8*cm, y, str(sale_data['quantity']))
        c.drawString(12*cm, y, f"{sale_data['price']:,.0f} FCFA")
        total = sale_data['quantity'] * sale_data['price']
        c.drawString(16*cm, y, f"{total:,.0f} FCFA")
        
        # Total
        y -= 2*cm
        c.setFont("Helvetica-Bold", 12)
        c.drawString(12*cm, y, "TOTAL:")
        c.drawString(16*cm, y, f"{total:,.0f} FCFA")
        
        # Signature
        c.setFont("Helvetica-Italic", 10)
        c.drawString(2*cm, 5*cm, "Signature du vendeur:")
        c.drawString(12*cm, 5*cm, "Signature du client:")
        
        c.save()
        return filename