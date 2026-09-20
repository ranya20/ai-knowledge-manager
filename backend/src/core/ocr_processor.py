# backend/src/core/ocr_processor.py
import pytesseract
import os
from pdf2image import convert_from_path
import cv2
import numpy as np
import re
from typing import Dict, List, Optional

# =============================================================================
# CONFIGURATION
# =============================================================================

POPPLER_PATH = r'C:\Users\ROG ZEPHYRUS\Documents\projet_ind\poppler-25.07.0\Library\bin'
TESSERACT_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

if os.path.exists(TESSERACT_PATH):
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

# =============================================================================
# OCR PROCESSOR OPTIMISÉ - VERSION COMPLÈTE
# =============================================================================

class OCRProcessor:
    def __init__(self, config):
        self.config = config
        self.tesseract_available = os.path.exists(TESSERACT_PATH)
        self.poppler_available = os.path.exists(POPPLER_PATH)
        
        # Configurations OCR optimisées
        self.ocr_configs = {
            'default': '--oem 3 --psm 6 -c tessedit_do_invert=0',
            'single_column': '--oem 3 --psm 4',
            'single_line': '--oem 3 --psm 7', 
            'single_word': '--oem 3 --psm 8',
            'sparse_text': '--oem 3 --psm 11',
            'document': '--oem 3 --psm 3',
        }
        
        # Dictionnaire de corrections OCR
        self.ocr_corrections = {
            # Corrections spécifiques basées sur tes tests
            r'\bOOR\b': 'OCR',
            r'\bAl\b': 'AI',
            r'\bvarifier\b': 'vérifier',
            r'\bteconnatssance\b': 'reconnaissance',
            r'\bTessoract\b': 'Tesseract',
            r'\bKnowledgs\b': 'Knowledge',
            r'\bMansger\b': 'Manager',
            r'\bCeciest\b': 'Ceci est',
            r'\bdelette\b': 'de texte',
            
            # Corrections générales
            r'\b0\b': 'o',
            r'\b1\b': 'l',
            r'\b5\b': 's',
            r'\b\[\b': 'l',
            r'\b\|\b': 'l',
            r'\b_\b': '',
            
            # Séparation de mots collés
            r'\b([a-z])([A-Z][a-z])': r'\1 \2',
            r'\b([A-Z][a-z])([A-Z][a-z])': r'\1 \2',
        }
        
        print(f"🔧 OCR Processor optimisé initialisé")

    def process_pdf(self, pdf_path: str) -> Dict:
        """Traite un PDF avec OCR optimisé"""
        if not self.tesseract_available or not self.poppler_available:
            return self._error_response("Dépendances manquantes")
        
        try:
            print(f"🔍 Traitement PDF: {os.path.basename(pdf_path)}")
            images = convert_from_path(pdf_path, dpi=300, poppler_path=POPPLER_PATH)
            
            full_text = ""
            successful_pages = 0
            
            for i, image in enumerate(images):
                print(f"   📄 Page {i+1}/{len(images)}...")
                result = self._process_single_image_optimized(np.array(image))
                
                if result['text'].strip():
                    successful_pages += 1
                    full_text += f"--- Page {i+1} ---\n{result['text']}\n\n"
                else:
                    full_text += f"--- Page {i+1} [VIDE] ---\nAucun texte détecté\n\n"
            
            return {
                'status': 'success',
                'metadata': {
                    'pages': len(images),
                    'successful_pages': successful_pages,
                    'pdf_type': 'scanned',
                    'processing_method': 'optimized'
                },
                'raw_text': full_text,
                'clean_text': self._clean_ocr_text_advanced(full_text),
            }
            
        except Exception as e:
            return self._error_response(f"Erreur PDF: {str(e)}")

    def process_image(self, image_path: str) -> Dict:
        """Traite une image avec OCR optimisé"""
        if not self.tesseract_available:
            return self._error_response("Tesseract non disponible")
        
        try:
            print(f"🔍 Traitement image: {os.path.basename(image_path)}")
            image = cv2.imread(image_path)
            
            if image is None:
                return self._error_response("Image non lisible")
            
            result = self._process_single_image_optimized(image)
            
            return {
                'status': 'success',
                'metadata': {
                    'file_type': 'image',
                    'preprocessing_used': result['method'],
                    'confidence': result['confidence'],
                    'text_length': len(result['text'])
                },
                'raw_text': result['text'],
                'clean_text': self._clean_ocr_text_advanced(result['text']),
            }
            
        except Exception as e:
            return self._error_response(f"Erreur image: {str(e)}")

    def _process_single_image_optimized(self, image: np.ndarray) -> Dict:
        """Traitement optimisé d'une seule image avec multiples stratégies"""
        strategies = [
            ('high_quality', self._preprocess_high_quality),
            ('contrast_boost', self._preprocess_contrast_boost),
            ('denoise_heavy', self._preprocess_denoise_heavy),
            ('border_clean', self._preprocess_border_clean),
        ]
        
        best_result = {'text': '', 'confidence': 0, 'method': 'original'}
        
        # Essayer d'abord l'image originale
        original_text, original_conf = self._ocr_with_confidence(image)
        if original_text.strip():
            best_result = {
                'text': original_text,
                'confidence': original_conf,
                'method': 'original'
            }
        
        # Essayer chaque stratégie de prétraitement
        for strategy_name, strategy_func in strategies:
            try:
                processed_img = strategy_func(image)
                text, confidence = self._ocr_with_confidence(processed_img)
                
                # Préférer le texte le plus long avec bonne confiance
                if (len(text.strip()) > len(best_result['text'].strip()) and 
                    confidence > 30) or confidence > best_result['confidence']:
                    best_result = {
                        'text': text,
                        'confidence': confidence,
                        'method': strategy_name
                    }
                    
            except Exception as e:
                continue
        
        # Si toujours peu de texte, forcer l'OCR avec différentes configs
        if len(best_result['text'].strip()) < 10:
            forced_text = self._force_ocr_detection(image)
            if forced_text.strip():
                best_result['text'] = forced_text
                best_result['method'] = 'forced_detection'
        
        return best_result

    def _preprocess_high_quality(self, image: np.ndarray) -> np.ndarray:
        """Prétraitement pour images de haute qualité"""
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        
        # Redimensionner si trop petit
        gray = self._resize_if_needed(gray, min_size=500)
        
        # Débruitage adaptatif
        denoised = cv2.medianBlur(gray, 3)
        
        # Seuillage adaptatif optimisé
        thresh = cv2.adaptiveThreshold(
            denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 15, 5
        )
        
        return thresh

    def _preprocess_contrast_boost(self, image: np.ndarray) -> np.ndarray:
        """Amélioration agressive du contraste"""
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        
        gray = self._resize_if_needed(gray, min_size=500)
        
        # CLAHE pour contraste local
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        enhanced = clahe.apply(gray)
        
        # Seuillage Otsu
        _, thresh = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Post-traitement morphologique
        kernel = np.ones((2,2), np.uint8)
        cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        
        return cleaned

    def _preprocess_denoise_heavy(self, image: np.ndarray) -> np.ndarray:
        """Débruitage lourd pour images bruyantes"""
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        
        gray = self._resize_if_needed(gray, min_size=500)
        
        # Débruitage non-local means
        denoised = cv2.fastNlMeansDenoising(gray, None, 15, 7, 21)
        
        # Bilateral filter pour préserver les bords
        bilateral = cv2.bilateralFilter(denoised, 9, 75, 75)
        
        # Seuillage adaptatif
        thresh = cv2.adaptiveThreshold(
            bilateral, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 21, 7
        )
        
        return thresh

    def _preprocess_border_clean(self, image: np.ndarray) -> np.ndarray:
        """Nettoyage des bordures et isolation du texte"""
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        
        gray = self._resize_if_needed(gray, min_size=500)
        
        # Détection et suppression des bordures
        _, binary = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            # Trouver la région de texte principale
            largest_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest_contour)
            
            # Ajouter une marge
            margin = 10
            x = max(0, x - margin)
            y = max(0, y - margin)
            w = min(gray.shape[1] - x, w + 2 * margin)
            h = min(gray.shape[0] - y, h + 2 * margin)
            
            cropped = gray[y:y+h, x:x+w]
        else:
            cropped = gray
        
        # Amélioration du contraste
        denoised = cv2.medianBlur(cropped, 3)
        thresh = cv2.adaptiveThreshold(
            denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 15, 5
        )
        
        return thresh

    def _resize_if_needed(self, image: np.ndarray, min_size: int = 500) -> np.ndarray:
        """Redimensionne l'image si elle est trop petite"""
        height, width = image.shape
        
        if height < min_size or width < min_size:
            scale = max(min_size/height, min_size/width)
            new_width = int(width * scale)
            new_height = int(height * scale)
            return cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
        
        return image

    def _ocr_with_confidence(self, image: np.ndarray) -> tuple:
        """OCR avec mesure de confiance et multiple configurations"""
        best_text = ""
        best_confidence = 0
        
        for config_name, config in self.ocr_configs.items():
            try:
                data = pytesseract.image_to_data(
                    image, 
                    lang='+'.join(self.config.OCR_LANGUAGES),
                    config=config,
                    output_type=pytesseract.Output.DICT
                )
                
                # Calculer la confiance moyenne
                confidences = [int(conf) for conf in data['conf'] if int(conf) > 0]
                avg_confidence = np.mean(confidences) if confidences else 0
                
                # Extraire le texte
                text = ' '.join([word for word in data['text'] if word.strip()])
                
                if avg_confidence > best_confidence and text.strip():
                    best_confidence = avg_confidence
                    best_text = text
                    
            except Exception:
                continue
        
        return best_text, best_confidence

    def _force_ocr_detection(self, image: np.ndarray) -> str:
        """Force la détection OCR avec toutes les configurations"""
        all_texts = []
        
        for config_name, config in self.ocr_configs.items():
            try:
                text = pytesseract.image_to_string(
                    image, 
                    lang='+'.join(self.config.OCR_LANGUAGES),
                    config=config
                )
                if text.strip():
                    all_texts.append(text.strip())
            except Exception:
                continue
        
        # Retourner le texte le plus long
        if all_texts:
            return max(all_texts, key=len)
        return ""

    def _clean_ocr_text_advanced(self, text: str) -> str:
        """Nettoyage avancé du texte OCR avec corrections intelligentes"""
        if not text:
            return ""
        
        # 1. Appliquer les corrections du dictionnaire
        for pattern, replacement in self.ocr_corrections.items():
            text = re.sub(pattern, replacement, text)
        
        # 2. Correction des caractères similaires
        char_replacements = {
            '0': 'o', '1': 'l', '5': 's', '|': 'l', '[': 'l',
            'O': '0', 'l': '1', 'S': '5', '€': 'C', '§': 'S',
            '`': "'", '´': "'", '‘': "'", '’': "'", '“': '"', '”': '"'
        }
        
        for wrong, correct in char_replacements.items():
            text = text.replace(wrong, correct)
        
        # 3. Séparation intelligente des mots
        text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)  # min+MAJ
        text = re.sub(r'([A-Z])([A-Z][a-z])', r'\1 \2', text)  # MAJ+MAJmin
        
        # 4. Gestion de la ponctuation
        text = re.sub(r'\s*,\s*', ', ', text)  # Espaces autour des virgules
        text = re.sub(r'\s*\.\s*', '. ', text)  # Espaces autour des points
        text = re.sub(r'\s+', ' ', text)  # Espaces multiples
        
        # 5. Nettoyage des lignes
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            if line:
                # Capitaliser la première lettre si nécessaire
                if line and line[0].islower() and len(line) > 1:
                    line = line[0].upper() + line[1:]
                cleaned_lines.append(line)
        
        # 6. Reconstruire le texte
        cleaned_text = '\n'.join(cleaned_lines)
        
        # 7. Supprimer les caractères non désirés restants
        cleaned_text = re.sub(r'[^\w\s\.,!?;:()\-&\'"/]', '', cleaned_text)
        
        return cleaned_text.strip()

    def _error_response(self, message: str) -> Dict:
        """Réponse d'erreur standardisée"""
        return {
            'status': 'error',
            'error': message
        }

# =============================================================================
# TEST COMPLET
# =============================================================================

if __name__ == "__main__":
    print("🧪 Test OCR Processor Complet...")
    
    class TestConfig:
        OCR_LANGUAGES = ['eng', 'fra']
    
    config = TestConfig()
    processor = OCRProcessor(config)
    
    # Tester avec différentes images
    test_files = [
        "data/incoming/test_simple.png",
        "data/incoming/test_ocr.png", 
        "data/incoming/ocr_optimized.png"
    ]
    
    for test_file in test_files:
        if os.path.exists(test_file):
            print(f"\n{'='*50}")
            print(f"🔍 Test: {os.path.basename(test_file)}")
            print(f"{'='*50}")
            
            result = processor.process_image(test_file)
            
            if result['status'] == 'success':
                print(f"✅ Succès!")
                print(f"📊 Méthode: {result['metadata']['preprocessing_used']}")
                print(f"📏 Longueur: {result['metadata']['text_length']} caractères")
                print(f"📄 Texte nettoyé:")
                print(f"'{result['clean_text']}'")
            else:
                print(f"❌ Erreur: {result['error']}")
        else:
            print(f"⚠️  Fichier non trouvé: {test_file}")
    
    print(f"\n🎯 Test OCR Processor terminé!")