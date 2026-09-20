import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.llm_integration import LLMIntegration
import config

def test_openrouter_complete():
    print("🧪 Test complet OpenRouter...\n")
    
    try:
        # Initialisation
        cfg = config.config
        llm = LLMIntegration(cfg)
        
        print(f"🤖 Provider: {cfg.LLM_PROVIDER}")
        print(f"📋 Modèle: {cfg.OPENROUTER_MODEL}")
        print()
        
        # Test de connexion simple
        print("1. 🔗 Test de connexion...")
        test_response = llm.provider.generate_response("Dis 'Bonjour' en une phrase.")
        print(f"   Réponse: {test_response}")
        print()
        
        # Test de résumé
        print("2. 📝 Test de résumé...")
        sample_text = """
        L'apprentissage profond (deep learning) est une sous-catégorie de l'apprentissage automatique 
        qui utilise des réseaux de neurones artificiels avec plusieurs couches. Ces réseaux sont 
        capables d'apprendre des représentations de données à différents niveaux d'abstraction.
        """
        summary = llm.generate_summary(sample_text)
        print(f"   Résumé: {summary}")
        print()
        
        # Test d'extraction de mots-clés
        print("3. 🔑 Test d'extraction de mots-clés...")
        keywords = llm.extract_keywords(sample_text)
        print(f"   Mots-clés: {', '.join(keywords)}")
        print()
        
        # Test RAG
        print("4. 🔍 Test RAG...")
        context_docs = [
            {
                'content': sample_text,
                'metadata': {'file_name': 'document_ia.pdf'}
            }
        ]
        rag_response = llm.generate_rag_response(
            "Qu'est-ce que l'apprentissage profond ?", 
            context_docs
        )
        print(f"   Question: Qu'est-ce que l'apprentissage profond ?")
        print(f"   Réponse RAG: {rag_response}")
        print()
        
        print("✅ Tous les tests passés avec succès !")
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_openrouter_complete()