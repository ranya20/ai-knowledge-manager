import os
from typing import Optional

class Config:
    # ==================== CHEMINS DES DOSSIERS ====================
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, "data")
    INCOMING_DIR = os.path.join(DATA_DIR, "incoming")
    PROCESSING_DIR = os.path.join(DATA_DIR, "processing") 
    PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
    FAILED_DIR = os.path.join(DATA_DIR, "failed")
    VECTOR_STORE_PATH = os.path.join(DATA_DIR, "vector_store")
    
    # ==================== FORMATS SUPPORTÃ‰S ====================
    SUPPORTED_FORMATS = {
        'pdf': ['.pdf'],
        'images': ['.jpg', '.jpeg', '.png', '.tiff', '.bmp'],
        'text': ['.txt', '.md'],
        'documents': ['.docx']
    }
    
    ALL_SUPPORTED_FORMATS = ['.pdf', '.jpg', '.jpeg', '.png', '.tiff', '.bmp', '.txt', '.md', '.docx']
    
    # ==================== PARAMÃˆTRES OCR ====================
    OCR_DPI = 300
    OCR_LANGUAGES = ['fra', 'eng']
    
    # ==================== MODÃˆLES D'EMBEDDING ====================
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"
    EMBEDDING_DIMENSION = 384
    
    # ==================== CONFIGURATION LLM ====================
    # Choix du fournisseur: "openrouter", "openai", "ollama", "huggingface", "none"
    LLM_PROVIDER = "openrouter"
    
    # === Configuration OpenRouter ===
    OPENROUTER_API_KEY = "VOTRE_CLE_OPENROUTER_ICI"
    OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
    OPENROUTER_MODEL = "meta-llama/llama-3.1-8b-instruct"  # ModÃ¨le fiable et rapide
    OPENROUTER_MAX_TOKENS = 2000
    OPENROUTER_TEMPERATURE = 0.7
    OPENROUTER_TIMEOUT = 60
    
    # === Configuration OpenAI (fallback) ===
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = "gpt-3.5-turbo"
    OPENAI_MAX_TOKENS = 1500
    OPENAI_TEMPERATURE = 0.3
    OPENAI_TIMEOUT = 30
    
    # === Configuration Ollama ===
    OLLAMA_BASE_URL = "http://localhost:11434"
    OLLAMA_MODEL = "llama2"
    OLLAMA_TIMEOUT = 60
    
    # === Configuration Hugging Face ===
    HUGGINGFACE_API_KEY: Optional[str] = os.getenv("HUGGINGFACE_API_KEY")
    HUGGINGFACE_MODEL = "microsoft/DialoGPT-large"
    
    # ==================== PARAMÃˆTRES RAG ====================
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 100
    MAX_CHUNKS_PER_DOCUMENT = 50
    SIMILARITY_THRESHOLD = 0.3
    MAX_CONTEXT_DOCS = 5
    SEARCH_TOP_K = 10
    
    # ==================== PARAMÃˆTRES DE TRAITEMENT ====================
    MAX_FILE_SIZE = 50 * 1024 * 1024
    MAX_CONTENT_LENGTH = 2_000_000
    BATCH_SIZE = 10
    PROCESSING_TIMEOUT = 300
    
    # ==================== MODÃˆLES OPENROUTER DISPONIBLES ====================
    OPENROUTER_MODELS = {
        # Mistral AI (recommandÃ© - fiable et rapide)
        "mistralai/mistral-7b-instruct": "Mistral 7B Instruct",
        "mistralai/mixtral-8x7b-instruct": "Mixtral 8x7B Instruct",
        
        # Google
        "google/gemini-pro": "Google Gemini Pro",
        "google/gemini-pro-vision": "Google Gemini Pro Vision",
        
        # Anthropic
        "anthropic/claude-2": "Claude 2",
        "anthropic/claude-instant-v1": "Claude Instant",
        
        # Meta
        "meta-llama/llama-3.1-8b-instruct": "Llama 3.1 8B Instruct",
        "meta-llama/llama-2-13b-chat": "Llama 2 13B Chat",
        "meta-llama/llama-2-70b-chat": "Llama 2 70B Chat",
        
        # OpenAI
        "openai/gpt-3.5-turbo": "GPT-3.5 Turbo",
        "openai/gpt-4": "GPT-4",
        
        # Autres
        "microsoft/wizardlm-2-8x22b": "WizardLM 2 8x22B",
        "nousresearch/nous-hermes-2-mixtral-8x7b-dpo": "Nous Hermes 2 Mixtral"
    }
    
    def __init__(self):
        """Initialise la configuration et crÃ©e les dossiers nÃ©cessaires"""
        self._create_directories()
        self._validate_config()
    
    def _create_directories(self):
        """CrÃ©e tous les dossiers nÃ©cessaires s'ils n'existent pas"""
        directories = [
            self.DATA_DIR,
            self.INCOMING_DIR,
            self.PROCESSING_DIR,
            self.PROCESSED_DIR,
            self.FAILED_DIR,
            self.VECTOR_STORE_PATH
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            print(f"âœ… Dossier vÃ©rifiÃ©/crÃ©Ã©: {directory}")
    
    def _validate_config(self):
        """Valide la configuration et affiche des avertissements"""
        warnings = []
        
        if self.LLM_PROVIDER == "openrouter":
            if not self.OPENROUTER_API_KEY or self.OPENROUTER_API_KEY = "VOTRE_CLE_OPENROUTER_ICI"
                warnings.append("âš ï¸  OPENROUTER_API_KEY non configurÃ©e")
            else:
                print(f"âœ… OpenRouter configurÃ© avec le modÃ¨le: {self.OPENROUTER_MODEL}")
            
            if self.OPENROUTER_MODEL not in self.OPENROUTER_MODELS:
                warnings.append(f"âš ï¸  ModÃ¨le OpenRouter inconnu: {self.OPENROUTER_MODEL}")
        
        elif self.LLM_PROVIDER == "openai":
            if not self.OPENAI_API_KEY:
                warnings.append("âš ï¸  OPENAI_API_KEY non configurÃ©e")
        
        elif self.LLM_PROVIDER == "huggingface":
            if not self.HUGGINGFACE_API_KEY:
                warnings.append("âš ï¸  HUGGINGFACE_API_KEY non configurÃ©e")
        
        elif self.LLM_PROVIDER == "ollama":
            print("ðŸ”— Utilisation d'Ollama - Assurez-vous qu'Ollama est en cours d'exÃ©cution")
        
        elif self.LLM_PROVIDER == "none":
            print("ðŸ”¶ Mode sans LLM - Seules les fonctionnalitÃ©s de base seront disponibles")
        
        else:
            warnings.append(f"âš ï¸  Fournisseur LLM inconnu: {self.LLM_PROVIDER}")
        
        # Afficher les avertissements
        for warning in warnings:
            print(warning)
    
    def get_llm_config(self) -> dict:
        """Retourne la configuration LLM sous forme de dictionnaire"""
        return {
            'provider': self.LLM_PROVIDER,
            'openrouter': {
                'api_key': self.OPENROUTER_API_KEY,
                'base_url': self.OPENROUTER_BASE_URL,
                'model': self.OPENROUTER_MODEL,
                'max_tokens': self.OPENROUTER_MAX_TOKENS,
                'temperature': self.OPENROUTER_TEMPERATURE,
                'timeout': self.OPENROUTER_TIMEOUT,
                'available_models': self.OPENROUTER_MODELS
            },
            'openai': {
                'api_key': self.OPENAI_API_KEY,
                'model': self.OPENAI_MODEL,
                'max_tokens': self.OPENAI_MAX_TOKENS,
                'temperature': self.OPENAI_TEMPERATURE,
                'timeout': self.OPENAI_TIMEOUT
            },
            'ollama': {
                'base_url': self.OLLAMA_BASE_URL,
                'model': self.OLLAMA_MODEL,
                'timeout': self.OLLAMA_TIMEOUT
            },
            'huggingface': {
                'api_key': self.HUGGINGFACE_API_KEY,
                'model': self.HUGGINGFACE_MODEL
            }
        }
    
    def get_rag_config(self) -> dict:
        """Retourne la configuration RAG sous forme de dictionnaire"""
        return {
            'chunk_size': self.CHUNK_SIZE,
            'chunk_overlap': self.CHUNK_OVERLAP,
            'similarity_threshold': self.SIMILARITY_THRESHOLD,
            'max_context_docs': self.MAX_CONTEXT_DOCS,
            'search_top_k': self.SEARCH_TOP_K,
            'embedding_model': self.EMBEDDING_MODEL
        }
    
    def __str__(self) -> str:
        """ReprÃ©sentation textuelle de la configuration"""
        return f"""
Configuration du SystÃ¨me RAG:
-----------------------------
ðŸ“ Dossiers:
  - DonnÃ©es: {self.DATA_DIR}
  - Vector Store: {self.VECTOR_STORE_PATH}

ðŸ¤– LLM:
  - Fournisseur: {self.LLM_PROVIDER}
  - ModÃ¨le: {self.OPENROUTER_MODEL if self.LLM_PROVIDER == 'openrouter' else self.OPENAI_MODEL}

ðŸ” RAG:
  - Taille des chunks: {self.CHUNK_SIZE}
  - Seuil de similaritÃ©: {self.SIMILARITY_THRESHOLD}
  - Documents max en contexte: {self.MAX_CONTEXT_DOCS}

ðŸ“„ Formats supportÃ©s: {', '.join(self.ALL_SUPPORTED_FORMATS)}
        """.strip()

# Instance globale de configuration
config = Config()

# Test de la configuration
if __name__ == "__main__":
    print("ðŸ§ª Test de la configuration...")
    print(config)
