import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.qa_engine import QAEngine
from src.core.document_processor import DocumentProcessor
import config

def test_rag_system():
    print("🧪 TEST SYSTÈME RAG COMPLET\n")
    
    try:
        # Initialisation
        qa_engine = QAEngine(config.config)
        processor = DocumentProcessor(config.config)
        
        print("1. 📊 Initialisation système:")
        stats = qa_engine.get_system_stats()
        print(f"   - Documents: {stats['vector_store']['total_documents']}")
        print(f"   - Embeddings: {stats['vector_store']['total_embeddings']}")
        print(f"   - Provider LLM: {stats['llm_provider']}")
        
        # DEBUG: Voir le contenu des documents
        print(f"\n🔍 DEBUG: Analyse des documents chargés:")
        for i, doc in enumerate(processor.vector_store.documents[:3]):
            metadata = doc.get('metadata', {})
            content_preview = str(doc.get('content', 'VIDE'))[:100]
            print(f"   Doc {i}: {metadata.get('file_name', 'SANS_NOM')}")
            print(f"     Contenu: {content_preview}...")
            print(f"     Métadonnées keys: {list(metadata.keys())}")
        
        # Test questions-réponses adaptées à VOS documents
        print("\n2. ❓ TEST QUESTIONS-RÉPONSES (adaptées à vos documents):")
        
        test_questions = [
            "Qui est Olympe de Gouges ?",
            "De quoi parle la Déclaration des droits de la femme ?", 
            "Quels sont les droits des femmes selon ce document ?",
            "Quel est le contexte historique de ce texte ?",
            "Quand ce document a-t-il été écrit ?"
        ]
        
        for i, question in enumerate(test_questions, 1):
            print(f"\n   {i}. Q: {question}")
            result = qa_engine.ask_question(question)
            
            print(f"      A: {result['answer'][:150]}...")
            print(f"      📚 Sources: {result['source_files']}")
            print(f"      🔍 Documents utilisés: {result['search_stats']['documents_after_filter']}")
        
        # Test recherche par sujet adapté
        print(f"\n3. 🔍 RECHERCHE PAR SUJET (adapté):")
        topics = ["femme", "droit", "histoire", "révolution"]
        
        for topic in topics:
            files = qa_engine.search_files_by_topic(topic)
            print(f"   '{topic}' → {len(files)} fichiers trouvés")
            for file in files[:2]:
                print(f"     - {file.get('file_name', 'Inconnu')} (score: {file.get('score', 0)})")
        
        print("\n✅ Test système RAG réussi!")
        
    except Exception as e:
        print(f"❌ Erreur système RAG: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_rag_system()