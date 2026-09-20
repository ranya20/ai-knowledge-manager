import os
import sys
import json
import shutil
from datetime import datetime
from typing import Dict, Any, List

# Ajouter le chemin pour les imports
backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from src.core.pdf_processor import PDFTypeDetector, TextPDFProcessor
from src.core.ocr_processor import OCRProcessor
from src.core.text_cleaner import TextCleaner
from src.core.vector_store import VectorStore
from src.core.llm_integration import LLMIntegration

class DocumentProcessor:
    def __init__(self, config):
        self.config = config
        self.type_detector = PDFTypeDetector()
        self.text_processor = TextPDFProcessor()
        self.ocr_processor = OCRProcessor(config)
        self.text_cleaner = TextCleaner()
        self.vector_store = VectorStore(config)
        self.llm = LLMIntegration(config)
        
        print("✅ DocumentProcessor initialisé avec RAG et Vector Store")
    
    def _move_processed_file(self, file_path: str, success: bool = True) -> str:
        """
        Déplace le fichier traité vers le dossier approprié
        """
        try:
            filename = os.path.basename(file_path)
            
            if success:
                # Déplacer vers processed
                destination_dir = self.config.PROCESSED_DIR
                print(f"✅ Déplacement vers processed: {filename}")
            else:
                # Déplacer vers failed
                destination_dir = self.config.FAILED_DIR
                print(f"❌ Déplacement vers failed: {filename}")
            
            # Créer le chemin de destination
            destination_path = os.path.join(destination_dir, filename)
            
            # S'assurer que le dossier de destination existe
            os.makedirs(destination_dir, exist_ok=True)
            
            # Déplacer le fichier
            shutil.move(file_path, destination_path)
            
            return destination_path
            
        except Exception as e:
            print(f"⚠️ Impossible de déplacer le fichier: {e}")
            return file_path

    def process_file(self, file_path: str) -> Dict[str, Any]:
        """Traite n'importe quel fichier supporté avec extraction complète"""
        filename = os.path.basename(file_path)
        file_ext = os.path.splitext(filename)[1].lower()
        
        print(f"🔍 Début traitement: {filename}")
        
        try:
            # Vérifier que le fichier existe
            if not os.path.exists(file_path):
                return {
                    'status': 'error',
                    'error': f'Fichier non trouvé: {file_path}'
                }
            
            # Traitement selon le type de fichier
            if file_ext == '.pdf':
                result = self._process_pdf(file_path)
            elif file_ext in self.config.SUPPORTED_FORMATS['images']:
                result = self._process_image(file_path)
            elif file_ext in ['.txt', '.md']:
                result = self._process_text_file(file_path)
            else:
                return {
                    'status': 'error',
                    'error': f'Format non supporté: {file_ext}'
                }
            
            # Déterminer si le traitement a réussi
            processing_success = result.get('status') == 'success'
            
            # Si le traitement a réussi, ajouter au vector store
            if processing_success:
                # Utiliser clean_text si disponible, sinon raw_text
                text_content = result.get('clean_text') or result.get('raw_text') or result.get('text', '')
                
                if text_content:
                    rag_result = self._process_with_rag(text_content, file_path, file_ext)
                    result.update(rag_result)
                    # Le succès RAG est requis pour considérer le traitement complet
                    processing_success = rag_result.get('rag_processed', False)
            
            # ✅ DÉPLACER LE FICHIER
            final_path = self._move_processed_file(file_path, processing_success)
            result['final_location'] = final_path
            
            return result
            
        except Exception as e:
            error_msg = f"Erreur lors du traitement: {str(e)}"
            print(f"❌ {error_msg}")
            
            # ✅ Même en cas d'erreur, déplacer le fichier vers failed
            final_path = self._move_processed_file(file_path, False)
            
            return {
                'status': 'error',
                'error': error_msg,
                'file_path': file_path,
                'final_location': final_path
            }
    
    def _process_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """Traite un PDF (détection automatique du type)"""
        try:
            pdf_type = self.type_detector.detect(pdf_path)
            print(f"📄 Type PDF détecté: {pdf_type}")
            
            if pdf_type in ['text', 'mixed']:
                result = self.text_processor.process(pdf_path)
            else:
                result = self.ocr_processor.process_pdf(pdf_path)
            
            # Nettoyer le texte extrait si nécessaire
            if result.get('status') == 'success':
                raw_text = result.get('raw_text') or result.get('text', '')
                if raw_text:
                    result['cleaned_text'] = self.text_cleaner.clean_text(raw_text)
                    result['text_length'] = len(result['cleaned_text'])
                    print(f"✅ PDF traité: {result['text_length']} caractères")
            
            return result
            
        except Exception as e:
            return {
                'status': 'error',
                'error': f"Erreur traitement PDF: {str(e)}",
                'file_path': pdf_path
            }
    
    def _process_image(self, image_path: str) -> Dict[str, Any]:
        """Traite une image scannée"""
        try:
            result = self.ocr_processor.process_image(image_path)
            
            # Nettoyer le texte extrait
            if result.get('status') == 'success':
                raw_text = result.get('raw_text') or result.get('text', '')
                if raw_text:
                    result['cleaned_text'] = self.text_cleaner.clean_text(raw_text)
                    result['text_length'] = len(result['cleaned_text'])
                    print(f"✅ Image traitée: {result['text_length']} caractères")
            
            return result
            
        except Exception as e:
            return {
                'status': 'error',
                'error': f"Erreur traitement image: {str(e)}",
                'file_path': image_path
            }
    
    def _process_text_file(self, text_path: str) -> Dict[str, Any]:
        """Traite un fichier texte simple avec gestion robuste des encodings"""
        try:
            print(f"📖 Lecture fichier texte: {os.path.basename(text_path)}")
            
            # Essayer différents encodings courants
            encodings = ['utf-8', 'latin-1', 'windows-1252', 'cp1252', 'iso-8859-1']
            
            text = None
            used_encoding = None
            
            for encoding in encodings:
                try:
                    with open(text_path, 'r', encoding=encoding) as f:
                        text = f.read()
                    used_encoding = encoding
                    print(f"   ✅ Encoding détecté: {encoding}")
                    break
                except UnicodeDecodeError:
                    continue
                except Exception as e:
                    continue
            
            # Si tous les encodings échouent, essayer en mode binaire avec replacement
            if text is None:
                try:
                    with open(text_path, 'rb') as f:
                        binary_content = f.read()
                    text = binary_content.decode('utf-8', errors='replace')
                    used_encoding = 'utf-8-with-replace'
                    print(f"   ⚠️  Encoding forcé avec replacement")
                except Exception as e:
                    return {
                        'status': 'error',
                        'error': f"Impossible de lire le fichier: {str(e)}",
                        'file_path': text_path
                    }
            
            # Vérifier que le texte n'est pas vide
            if not text or len(text.strip()) == 0:
                return {
                    'status': 'error',
                    'error': 'Fichier texte vide',
                    'file_path': text_path
                }
            
            cleaned_text = self.text_cleaner.clean_text(text)
            print(f"   📊 Texte nettoyé: {len(cleaned_text)} caractères")
            
            return {
                'status': 'success',
                'text': text,
                'cleaned_text': cleaned_text,
                'text_length': len(cleaned_text),
                'file_path': text_path,
                'file_type': 'text',
                'encoding': used_encoding
            }
            
        except Exception as e:
            error_msg = f"Erreur lecture fichier texte: {str(e)}"
            print(f"❌ {error_msg}")
            return {
                'status': 'error',
                'error': error_msg,
                'file_path': text_path
            }
    
    def _process_with_rag(self, text: str, file_path: str, file_ext: str) -> Dict[str, Any]:
        """
        Traite le texte avec le système RAG : résumé, mots-clés et stockage vectoriel
        """
        try:
            filename = os.path.basename(file_path)
            print(f"🤖 Traitement RAG pour: {filename}")
            
            # Préparer les métadonnées
            metadata = {
                'file_name': filename,
                'file_path': file_path,
                'file_type': file_ext,
                'file_size': os.path.getsize(file_path),
                'processing_date': datetime.now().isoformat(),
                'content_length': len(text)
            }
            
            # Générer un résumé avec LLM
            print("📝 Génération du résumé...")
            summary = self.llm.generate_summary(text)
            metadata['summary'] = summary
            
            # Extraire les mots-clés avec LLM
            print("🔑 Extraction des mots-clés...")
            keywords = self.llm.extract_keywords(text)
            metadata['keywords'] = keywords
            
            # Ajouter au vector store (gère automatiquement le chunking)
            print("💾 Ajout au vector store...")
            success = self.vector_store.add_document(text, metadata)
            
            if success:
                # Récupérer les statistiques mises à jour
                stats = self.vector_store.get_stats()
                
                return {
                    'rag_processed': True,
                    'summary': summary,
                    'keywords': keywords,
                    'vector_store_success': True,
                    'total_documents': stats['total_documents'],
                    'unique_files': stats['unique_files']
                }
            else:
                return {
                    'rag_processed': False,
                    'vector_store_success': False,
                    'error': 'Échec de l\'ajout au vector store'
                }
                
        except Exception as e:
            error_msg = f"Erreur traitement RAG: {str(e)}"
            print(f"❌ {error_msg}")
            return {
                'rag_processed': False,
                'error': error_msg
            }
    
    def process_document(self, file_path: str) -> Dict[str, Any]:
        """
        Alias pour compatibilité avec l'ancien code
        """
        result = self.process_file(file_path)
        
        # Formater le résultat pour la compatibilité
        if result.get('status') == 'success':
            return {
                'success': True,
                'file_name': os.path.basename(file_path),
                'content_length': result.get('text_length', 0),
                'summary': result.get('summary', ''),
                'keywords': result.get('keywords', []),
                'rag_processed': result.get('rag_processed', False)
            }
        else:
            return {
                'success': False,
                'error': result.get('error', 'Erreur inconnue'),
                'file_path': file_path
            }