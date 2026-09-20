# backend/create_test_pdf.py
from fpdf import FPDF
import os

def create_sample_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.cell(200, 10, txt="Test Document pour AI Knowledge Manager", ln=1, align='C')
    pdf.ln(10)
    
    pdf.multi_cell(0, 10, txt="Ceci est un document de test pour vérifier le fonctionnement du système.")
    pdf.ln(5)
    pdf.multi_cell(0, 10, txt="Il contient du texte sélectionnable pour tester l'extraction PDF.")
    pdf.ln(5)
    pdf.multi_cell(0, 10, txt="Page 1 - Fin du document test.")
    
    # Sauvegarder
    os.makedirs('data/incoming', exist_ok=True)
    pdf.output('data/incoming/test_valid.pdf')
    print("✅ PDF de test créé: data/incoming/test_valid.pdf")

if __name__ == "__main__":
    create_sample_pdf()