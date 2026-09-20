# backend/create_test_image.py
from PIL import Image, ImageDraw, ImageFont
import os

def create_test_image():
    # Créer une image blanche
    img = Image.new('RGB', (800, 400), color='white')
    d = ImageDraw.Draw(img)
    
    # Ajouter du texte
    text = """Test OCR AI Knowledge Manager
Ceci est une image de test
pour vérifier la reconnaissance de texte
avec Tesseract OCR"""
    
    # Dessiner le texte
    d.text((50, 50), text, fill='black')
    
    # Sauvegarder
    os.makedirs('data/incoming', exist_ok=True)
    img.save('data/incoming/test_ocr.png')
    print("✅ Image de test créée: data/incoming/test_ocr.png")

if __name__ == "__main__":
    create_test_image()