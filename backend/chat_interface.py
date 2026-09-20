
from src.core.qa_engine import QAEngine
import config

def chat_interface():
    print("🤖 ASSISTANT RAG - Interface de Chat")
    print("=" * 50)
    print("Tapez 'quit' pour sortir, 'stats' pour les statistiques")
    
    qa_engine = QAEngine(config.config)
    
    while True:
        question = input("\n❓ Question: ").strip()
        
        if question.lower() in ['quit', 'exit', 'q']:
            print("👋 Au revoir !")
            break
        elif question.lower() in ['stats', 'statistiques']:
            stats = qa_engine.get_system_stats()
            print(f"📊 Statistiques système:")
            print(f"   - Documents: {stats['vector_store']['total_documents']}")
            print(f"   - Fichiers uniques: {stats['vector_store']['unique_files']}")
            print(f"   - Embeddings: {stats['vector_store']['total_embeddings']}")
            continue
        elif not question:
            continue
            
        print("🔍 Recherche en cours...")
        try:
            result = qa_engine.ask_question(question)
            print(f"\n🤖 Réponse: {result['answer']}")
            if result['source_files']:
                print(f"📚 Sources: {', '.join(result['source_files'])}")
            else:
                print("📚 Aucune source identifiée")
                
            print(f"🔍 Documents utilisés: {result['search_stats']['documents_after_filter']}")
            
        except Exception as e:
            print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    chat_interface()
