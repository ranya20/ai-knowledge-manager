import os
import requests
import json
import time
from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod
from openai import OpenAI

class LLMProvider(ABC):
    """Interface abstraite pour les fournisseurs LLM"""
    
    @abstractmethod
    def generate_response(self, prompt: str, context: str = "", **kwargs) -> str:
        pass
    
    @abstractmethod
    def generate_chat_response(self, messages: List[Dict[str, str]], **kwargs) -> str:
        pass

class OpenRouterProvider(LLMProvider):
    """Provider pour OpenRouter avec support multiple modèles"""
    
    def __init__(self, api_key: str, base_url: str = "https://openrouter.ai/api/v1", 
                 model: str = "mistralai/mistral-7b-instruct", max_tokens: int = 2000, 
                 temperature: float = 0.7, timeout: int = 60):
        self.api_key = api_key
        print("API KEY USED IN CODE:", api_key)
        self.base_url = base_url
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.timeout = timeout
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            
            "X-Title": "AI Knowledge Manager"
        }
    
    def generate_response(self, prompt: str, context: str = "", **kwargs) -> str:
        """Génère une réponse avec OpenRouter"""
        if context:
            enhanced_prompt = f"Contexte: {context}\n\nQuestion: {prompt}"
        else:
            enhanced_prompt = prompt
            
        try:
            messages = [
                {
                    "role": "system",
                    "content": "Vous êtes un assistant IA utile qui fournit des réponses précises et concises en français."
                },
                {
                    "role": "user", 
                    "content": enhanced_prompt
                }
            ]
            
            return self._make_openrouter_request(messages, kwargs)
            
        except Exception as e:
            return f"Erreur OpenRouter: {str(e)}"
    
    def generate_chat_response(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Génère une réponse conversationnelle avec OpenRouter"""
        try:
            # S'assurer qu'il y a un message système
            if not any(msg.get('role') == 'system' for msg in messages):
                messages.insert(0, {
                    "role": "system",
                    "content": "Vous êtes un assistant IA utile qui fournit des réponses précises et concises en français."
                })
            
            return self._make_openrouter_request(messages, kwargs)
            
        except Exception as e:
            return f"Erreur OpenRouter Chat: {str(e)}"
    
    def _make_openrouter_request(self, messages: List[Dict[str, str]], kwargs: dict) -> str:
        """Fait une requête à l'API OpenRouter"""
        try:
            payload = {
                "model": kwargs.get('model', self.model),
                "messages": messages,
                "max_tokens": kwargs.get('max_tokens', self.max_tokens),
                "temperature": kwargs.get('temperature', self.temperature),
            }
            
            # Nettoyer le payload des valeurs None
            payload = {k: v for k, v in payload.items() if v is not None}
            
            print(f"🔍 Envoi requête OpenRouter avec le modèle: {payload['model']}")
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=kwargs.get('timeout', self.timeout)
            )
            
            # Debug: afficher la réponse brute en cas d'erreur
            if response.status_code != 200:
                error_msg = f"Erreur OpenRouter {response.status_code}: {response.text}"
                print(f"❌ {error_msg}")
                
                # Essayer d'extraire le message d'erreur détaillé
                try:
                    error_data = response.json()
                    if 'error' in error_data and 'message' in error_data['error']:
                        return f"Erreur OpenRouter: {error_data['error']['message']}"
                except:
                    pass
                    
                return error_msg
            
            data = response.json()
            
            if 'choices' in data and len(data['choices']) > 0:
                return data['choices'][0]['message']['content'].strip()
            elif 'error' in data:
                return f"Erreur OpenRouter: {data['error']}"
            else:
                return "Erreur: Format de réponse inattendu de OpenRouter"
            
        except requests.exceptions.Timeout:
            return "Erreur OpenRouter: Timeout - la requête a pris trop de temps"
        except requests.exceptions.RequestException as e:
            error_msg = f"Erreur OpenRouter (HTTP): {str(e)}"
            print(f"❌ {error_msg}")
            return error_msg
        except Exception as e:
            error_msg = f"Erreur OpenRouter: {str(e)}"
            print(f"❌ {error_msg}")
            return error_msg
    
    def get_available_models(self) -> List[Dict]:
        """Récupère la liste des modèles disponibles sur OpenRouter"""
        try:
            response = requests.get(
                f"{self.base_url}/models",
                headers=self.headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json().get('data', [])
        except Exception as e:
            print(f"Erreur lors de la récupération des modèles OpenRouter: {e}")
            return []

class OpenAIProvider(LLMProvider):
    """Provider pour OpenAI GPT"""
    
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo", max_tokens: int = 1000, temperature: float = 0.3):
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
    
    def generate_response(self, prompt: str, context: str = "", **kwargs) -> str:
        """Génère une réponse à partir d'un prompt simple"""
        if context:
            enhanced_prompt = f"Contexte: {context}\n\nQuestion: {prompt}\n\nRéponse:"
        else:
            enhanced_prompt = prompt
            
        try:
            response = self.client.completions.create(
                model=self.model,
                prompt=enhanced_prompt,
                max_tokens=kwargs.get('max_tokens', self.max_tokens),
                temperature=kwargs.get('temperature', self.temperature)
            )
            return response.choices[0].text.strip()
        except Exception as e:
            return f"Erreur OpenAI: {str(e)}"
    
    def generate_chat_response(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Génère une réponse dans un format conversationnel"""
        try:
            response = self.client.chat.completions.create(
                model=kwargs.get('model', self.model),
                messages=messages,
                max_tokens=kwargs.get('max_tokens', self.max_tokens),
                temperature=kwargs.get('temperature', self.temperature)
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Erreur OpenAI Chat: {str(e)}"

class OllamaProvider(LLMProvider):
    """Provider pour Ollama (modèles locaux)"""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama2"):
        self.base_url = base_url
        self.model = model
    
    def generate_response(self, prompt: str, context: str = "", **kwargs) -> str:
        """Génère une réponse avec Ollama"""
        if context:
            enhanced_prompt = f"Contexte: {context}\n\nQuestion: {prompt}"
        else:
            enhanced_prompt = prompt
            
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": kwargs.get('model', self.model),
                    "prompt": enhanced_prompt,
                    "stream": False
                },
                timeout=kwargs.get('timeout', 60)
            )
            response.raise_for_status()
            return response.json().get('response', '').strip()
        except Exception as e:
            return f"Erreur Ollama: {str(e)}"
    
    def generate_chat_response(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Génère une réponse conversationnelle avec Ollama"""
        try:
            # Convertir le format des messages pour Ollama
            prompt = self._format_messages_for_ollama(messages)
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": kwargs.get('model', self.model),
                    "prompt": prompt,
                    "stream": False
                },
                timeout=kwargs.get('timeout', 60)
            )
            response.raise_for_status()
            return response.json().get('response', '').strip()
        except Exception as e:
            return f"Erreur Ollama Chat: {str(e)}"
    
    def _format_messages_for_ollama(self, messages: List[Dict[str, str]]) -> str:
        """Formate les messages pour Ollama"""
        formatted = []
        for msg in messages:
            role = msg.get('role', 'user')
            content = msg.get('content', '')
            formatted.append(f"{role}: {content}")
        return "\n".join(formatted) + "\nassistant:"

class HuggingFaceProvider(LLMProvider):
    """Provider pour Hugging Face Inference API"""
    
    def __init__(self, api_key: str, model: str = "microsoft/DialoGPT-large"):
        self.api_key = api_key
        self.model = model
        self.headers = {"Authorization": f"Bearer {api_key}"}
    
    def generate_response(self, prompt: str, context: str = "", **kwargs) -> str:
        """Génère une réponse avec Hugging Face"""
        if context:
            enhanced_prompt = f"Contexte: {context}\n\nQuestion: {prompt}"
        else:
            enhanced_prompt = prompt
            
        try:
            response = requests.post(
                f"https://api-inference.huggingface.co/models/{self.model}",
                headers=self.headers,
                json={"inputs": enhanced_prompt}
            )
            response.raise_for_status()
            result = response.json()
            
            # Le format de réponse varie selon le modèle
            if isinstance(result, list) and len(result) > 0:
                if 'generated_text' in result[0]:
                    return result[0]['generated_text']
                else:
                    return str(result[0])
            elif isinstance(result, dict) and 'generated_text' in result:
                return result['generated_text']
            else:
                return str(result)
                
        except Exception as e:
            return f"Erreur HuggingFace: {str(e)}"
    
    def generate_chat_response(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Hugging Face a des modèles de chat spécifiques"""
        # Pour la simplicité, on utilise generate_response
        last_message = messages[-1]['content'] if messages else ""
        return self.generate_response(last_message)

class LLMIntegration:
    """Classe unifiée pour l'intégration LLM"""
    
    def __init__(self, config):
        self.config = config
        self.provider = self._initialize_provider()
    
    def _initialize_provider(self) -> LLMProvider:
        """Initialise le provider LLM selon la configuration"""
        provider = self.config.LLM_PROVIDER.lower()
        
        if provider == "openrouter":
            if not self.config.OPENROUTER_API_KEY:
                raise ValueError("OPENROUTER_API_KEY non configurée")
            print(f"🚀 Initialisation OpenRouter avec le modèle: {self.config.OPENROUTER_MODEL}")
            return OpenRouterProvider(
                api_key=self.config.OPENROUTER_API_KEY,
                base_url=self.config.OPENROUTER_BASE_URL,
                model=self.config.OPENROUTER_MODEL,
                max_tokens=self.config.OPENROUTER_MAX_TOKENS,
                temperature=self.config.OPENROUTER_TEMPERATURE,
                timeout=self.config.OPENROUTER_TIMEOUT
            )
        elif provider == "openai":
            if not self.config.OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY non configurée")
            return OpenAIProvider(
                api_key=self.config.OPENAI_API_KEY,
                model=self.config.OPENAI_MODEL,
                max_tokens=self.config.OPENAI_MAX_TOKENS,
                temperature=self.config.OPENAI_TEMPERATURE
            )
        elif provider == "ollama":
            print(f"🚀 Initialisation Ollama avec le modèle: {self.config.OLLAMA_MODEL}")
            return OllamaProvider(
                base_url=self.config.OLLAMA_BASE_URL,
                model=self.config.OLLAMA_MODEL
            )
        elif provider == "huggingface":
            if not self.config.HUGGINGFACE_API_KEY:
                raise ValueError("HUGGINGFACE_API_KEY non configurée")
            return HuggingFaceProvider(
                api_key=self.config.HUGGINGFACE_API_KEY,
                model=self.config.HUGGINGFACE_MODEL
            )
        elif provider == "none":
            print("🔶 Mode sans LLM activé - utilisation du mode basique")
            return self._create_dummy_provider()
        else:
            raise ValueError(f"Provider LLM non supporté: {provider}")
    
    def _create_dummy_provider(self) -> LLMProvider:
        """Crée un provider factice pour le mode sans LLM"""
        class DummyProvider(LLMProvider):
            def generate_response(self, prompt: str, context: str = "", **kwargs) -> str:
                if context:
                    return f"Mode sans LLM - Question: {prompt}\nContexte fourni: {context[:100]}..."
                return f"Mode sans LLM: {prompt}"
            
            def generate_chat_response(self, messages: List[Dict[str, str]], **kwargs) -> str:
                last_message = messages[-1]['content'] if messages else ""
                return f"Mode sans LLM: {last_message}"
        
        return DummyProvider()
    
    def generate_rag_response(self, question: str, context_docs: List[Dict], **kwargs) -> str:
        """Génère une réponse RAG avec contexte"""
        # Préparer le contexte
        context_text = self._prepare_context(context_docs)
        
        # Préparer le prompt RAG
        messages = [
            {
                "role": "system",
                "content": """Vous êtes un assistant IA utile qui répond aux questions basées sur le contexte fourni.
Répondez UNIQUEMENT en utilisant les informations du contexte. 
Si la réponse n'est pas dans le contexte, dites clairement "Je n'ai pas trouvé cette information dans les documents fournis."
Gardez vos réponses précises, factuelles et basées sur le contexte. Répondez en français.

Contexte des documents:
{context}"""
            },
            {
                "role": "user",
                "content": f"Question: {question}"
            }
        ]
        
        # Remplacer le placeholder {context} dans le message système
        messages[0]['content'] = messages[0]['content'].replace("{context}", context_text)
        
        return self.provider.generate_chat_response(messages, **kwargs)
    
    def generate_summary(self, text: str, **kwargs) -> str:
        """Génère un résumé avec LLM"""
        prompt = f"Résumez le texte suivant de manière concise et informative en français (max 150 mots):\n\n{text}"
        
        messages = [
            {
                "role": "system", 
                "content": "Vous êtes un assistant qui crée des résumés concis et informatifs en français."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
        
        return self.provider.generate_chat_response(messages, **kwargs)
    
    def extract_keywords(self, text: str, max_keywords: int = 10, **kwargs) -> List[str]:
        """Extrait les mots-clés avec LLM"""
        prompt = f"""Extrayez les {max_keywords} mots-clés les plus importants du texte suivant.
Retournez UNIQUEMENT les mots-clés en français séparés par des virgules, sans explication:

{text}"""
        
        response = self.provider.generate_response(prompt, **kwargs)
        # Nettoyer la réponse et extraire les mots-clés
        keywords = [kw.strip() for kw in response.split(',')]
        keywords = [kw for kw in keywords if kw and len(kw) > 1]  # Filtrer les éléments vides
        return keywords[:max_keywords]
    
    def analyze_sentiment(self, text: str, **kwargs) -> str:
        """Analyse le sentiment du texte avec LLM"""
        prompt = f"Analysez le sentiment du texte suivant (positif, négatif, neutre) et expliquez brièvement en français:\n\n{text}"
        
        messages = [
            {
                "role": "system",
                "content": "Vous êtes un analyste de sentiment. Fournissez une analyse concise en français."
            },
            {
                "role": "user", 
                "content": prompt
            }
        ]
        
        return self.provider.generate_chat_response(messages, **kwargs)
    
    def _prepare_context(self, context_docs: List[Dict]) -> str:
        """Prépare le contexte à partir des documents pertinents"""
        if not context_docs:
            return "Aucun document pertinent trouvé."
        
        context_parts = []
        
        for i, doc in enumerate(context_docs[:self.config.MAX_CONTEXT_DOCS]):
            source = doc.get('metadata', {}).get('file_name', 'Document')
            content = doc.get('content', '') or doc.get('chunk', '')
            
            context_parts.append(f"--- Document {i+1}: {source} ---\n{content}\n")
        
        return "\n".join(context_parts)
    
    def test_connection(self) -> Dict[str, Any]:
        """Teste la connexion au provider LLM"""
        try:
            start_time = time.time()
            response = self.provider.generate_response("Répondez simplement 'OK' pour confirmer la connexion.")
            end_time = time.time()
            
            return {
                'success': 'OK' in response.upper(),
                'response_time': round(end_time - start_time, 2),
                'response': response,
                'provider': self.config.LLM_PROVIDER
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'provider': self.config.LLM_PROVIDER
            }

# Test du module
if __name__ == "__main__":
    print("🧪 Test du module LLM Integration...")
    
    # Configuration de test
    class TestConfig:
        LLM_PROVIDER = "openrouter"
        OPENROUTER_API_KEY = "test_key"
        OPENROUTER_MODEL = "mistralai/mistral-7b-instruct"
        OPENROUTER_MAX_TOKENS = 2000
        OPENROUTER_TEMPERATURE = 0.7
        OPENROUTER_TIMEOUT = 60
        MAX_CONTEXT_DOCS = 5
    
    try:
        test_config = TestConfig()
        llm = LLMIntegration(test_config)
        print("✅ LLM Integration initialisé avec succès")
    except Exception as e:
        print(f"❌ Erreur d'initialisation: {e}")