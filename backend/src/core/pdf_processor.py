import PyPDF2
import os
import re

class PDFTypeDetector:
    @staticmethod
    def detect(pdf_path):
        """Détecte le type de PDF"""
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                total_pages = len(reader.pages)
                text_pages = 0
                
                sample_pages = min(5, total_pages)
                
                for i in range(sample_pages):
                    text = reader.pages[i].extract_text()
                    if len(text.strip()) > 100:
                        text_pages += 1
                
                text_ratio = text_pages / sample_pages
                
                if text_ratio > 0.8:
                    return 'text'
                elif text_ratio > 0.2:
                    return 'mixed'
                else:
                    return 'scanned'
                    
        except Exception as e:
            print(f"Erreur détection PDF {pdf_path}: {e}")
            return 'unknown'

class TextPDFProcessor:
    def process(self, pdf_path):
        """Traite un PDF avec texte sélectionnable"""
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                metadata = {
                    'title': reader.metadata.get('/Title', ''),
                    'author': reader.metadata.get('/Author', ''),
                    'pages': len(reader.pages),
                    'pdf_type': 'text'
                }
                
                full_text = ""
                for page_num, page in enumerate(reader.pages):
                    page_text = page.extract_text()
                    full_text += f"--- Page {page_num + 1} ---\n{page_text}\n\n"
                
                return {
                    'status': 'success',
                    'metadata': metadata,
                    'raw_text': full_text,
                    'clean_text': self._clean_text(full_text)
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def _clean_text(self, text):
        """Nettoie le texte extrait"""
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = re.sub(r'[^\x00-\x7F]+', ' ', text)
        return text.strip()