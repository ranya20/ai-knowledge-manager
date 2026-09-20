# backend/src/core/url_processor.py
import os
import re
import requests
from typing import Dict, Any, Optional
from urllib.parse import urlparse
from .llm_integration import LLMIntegration

class URLProcessor:
    """Processeur d'URLs pour extraire le contenu web avec LLM"""
    
    def __init__(self, config, llm_integration: LLMIntegration):
        self.config = config
        self.llm = llm_integration
        
    def extract_content(self, url: str) -> Dict[str, Any]:
        """
        Extrait le contenu d'une URL en utilisant le LLM
        
        Args:
            url: L'URL à traiter
            
        Returns:
            Dict avec le contenu extrait et les métadonnées
        """
        try:
            print(f"🌐 Extraction contenu URL: {url}")
            
            # Valider l'URL
            if not self._is_valid_url(url):
                return {
                    'success': False,
                    'error': 'URL invalide',
                    'url': url
                }
            
            # Préparer le prompt pour le LLM
            prompt = self._create_extraction_prompt(url)
            
            # Appeler le LLM pour extraire le contenu
            print("🤖 Appel LLM pour extraction du contenu...")
            extracted_content = self.llm.provider.generate_response(prompt)
            
            # Nettoyer et structurer la réponse
            cleaned_content = self._clean_extracted_content(extracted_content)
            
            # Générer un résumé immédiat
            summary = self.llm.generate_summary(cleaned_content, content_type="web")
            
            # Extraire les mots-clés
            keywords = self.llm.extract_keywords(cleaned_content)
            
            return {
                'success': True,
                'url': url,
                'content': cleaned_content,
                'summary': summary,
                'keywords': keywords,
                'content_length': len(cleaned_content),
                'domain': self._extract_domain(url)
            }
            
        except Exception as e:
            print(f"❌ Erreur extraction URL {url}: {e}")
            return {
                'success': False,
                'error': str(e),
                'url': url
            }
    
    def process_url_for_chat(self, url: str, question: str = "") -> Dict[str, Any]:
        """
        Traite une URL pour une réponse immédiate dans le chat
        
        Args:
            url: L'URL à analyser
            question: Question spécifique (optionnelle)
            
        Returns:
            Dict avec la réponse immédiate
        """
        try:
            # Extraire le contenu
            extraction_result = self.extract_content(url)
            
            if not extraction_result['success']:
                return extraction_result
            
            content = extraction_result['content']
            summary = extraction_result['summary']
            
            # Si une question est posée, répondre en contexte
            if question:
                response = self.llm.generate_rag_response(
                    question, 
                    [{'content': content, 'metadata': {'source': url}}]
                )
            else:
                # Sinon, utiliser le résumé
                response = f"**Résumé du contenu :**\n\n{summary}\n\n**Source :** {url}"
            
            return {
                'success': True,
                'url': url,
                'response': response,
                'summary': summary,
                'keywords': extraction_result['keywords'],
                'content_length': extraction_result['content_length']
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'url': url
            }
    
    def save_url_to_file(self, url: str, content: str) -> str:
        """
        Sauvegarde le contenu de l'URL dans un fichier texte
        
        Args:
            url: L'URL source
            content: Le contenu à sauvegarder
            
        Returns:
            Chemin du fichier créé
        """
        try:
            # Créer un nom de fichier sécurisé
            domain = self._extract_domain(url)
            safe_filename = f"url_{domain}_{hash(url) % 10000}.txt"
            file_path = os.path.join(self.config.INCOMING_DIR, safe_filename)
            
            # Ajouter les métadonnées en en-tête
            formatted_content = f"URL: {url}\nDomaine: {domain}\nExtraction: {os.path.basename(__file__)}\n\n{content}"
            
            # Sauvegarder le fichier
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(formatted_content)
            
            print(f"💾 Contenu sauvegardé: {file_path}")
            return file_path
            
        except Exception as e:
            print(f"❌ Erreur sauvegarde fichier: {e}")
            return None
    
    def _is_valid_url(self, url: str) -> bool:
        """Valide le format de l'URL"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False
    
    def _extract_domain(self, url: str) -> str:
        """Extrait le domaine de l'URL"""
        try:
            return urlparse(url).netloc.replace('.', '_')
        except:
            return "unknown"
    
    def _create_extraction_prompt(self, url: str) -> str:
        """Crée le prompt pour l'extraction LLM"""
        return f"""
        Visitez cette URL et extrayez TOUT le contenu texte important : {url}
        
        INSTRUCTIONS IMPORTANTES :
        1. Extrayez UNIQUEMENT le contenu principal (ignorez menus, pieds de page, publicités)
        2. Gardez la structure (titres, paragraphes, listes)
        3. Préservez le formatage de base
        4. Ne rajoutez PAS de commentaires
        5. Retournez le texte brut et structuré
        
        Si c'est une vidéo YouTube ou similaire, décrivez le contenu visuel et audio.
        Si c'est un article, extrayez le texte complet.
        Si c'est une page produit, extrayez les spécifications et descriptions.
        
        Retournez UNIQUEMENT le contenu extrait, sans introduction ni conclusion.
        """
    
    def _clean_extracted_content(self, content: str) -> str:
        """Nettoie le contenu extrait par le LLM"""
        # Supprimer les phrases d'introduction/confirmation du LLM
        patterns = [
            r"^.*?(?:contenu|texte|article|page).*?:\s*",
            r"^(?:Voici|Voilà|J'ai).*?:\s*",
            r"^---.*?---\s*"
        ]
        
        cleaned = content
        for pattern in patterns:
            cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE | re.MULTILINE)
        
        return cleaned.strip()

# Test du module
if __name__ == "__main__":
    print("🧪 Test URL Processor...")
    
    # Configuration de test
    class TestConfig:
        INCOMING_DIR = "data/incoming"
        LLM_PROVIDER = "openrouter"
        OPENROUTER_API_KEY = "test_key"
    
    try:
        from llm_integration import LLMIntegration
        config = TestConfig()
        llm = LLMIntegration(config)
        processor = URLProcessor(config, llm)
        
        # Test d'extraction
        test_url = "https://example.com"
        result = processor.extract_content(test_url)
        print(f"✅ Test extraction: {result.get('success', False)}")
        
    except Exception as e:
        print(f"❌ Erreur test: {e}")