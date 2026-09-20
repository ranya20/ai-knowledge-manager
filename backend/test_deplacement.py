import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.document_processor import DocumentProcessor
import config

def test_deplacement_fichiers():
    print("🧪 TEST DÉPLACEMENT DES FICHIERS")
    print("=" * 50)
    
    # Initialisation
    processor = DocumentProcessor(config.config)
    
    # Fichier de test
    test_file = "data/incoming/test_nouveau_document.txt"
    
    print(f"1. 📍 ÉTAT AVANT TRAITEMENT:")
    print(f"   - Fichier existe dans incoming: {os.path.exists(test_file)}")
    
    # Traitement du fichier
    print(f"\n2. 🔧 TRAITEMENT EN COURS...")
    result = processor.process_file(test_file)
    
    print(f"\n3. 📍 ÉTAT APRÈS TRAITEMENT:")
    print(f"   - Fichier dans incoming: {os.path.exists(test_file)}")
    print(f"   - Statut traitement: {result.get('status', 'N/A')}")
    print(f"   - Emplacement final: {result.get('final_location', 'N/A')}")
    print(f"   - Traitement RAG: {result.get('rag_processed', 'N/A')}")
    
    # Vérifier le dossier processed
    if os.path.exists("data/processed/test_nouveau_document.txt"):
        print(f"   - ✅ Fichier trouvé dans processed/")
    else:
        print(f"   - ❌ Fichier NON trouvé dans processed/")
    
    # Vérifier les stats vector store
    stats = processor.vector_store.get_stats()
    print(f"\n4. 📊 VECTOR STORE:")
    print(f"   - Documents totaux: {stats['total_documents']}")
    print(f"   - Fichiers uniques: {stats['unique_files']}")

if __name__ == "__main__":
    test_deplacement_fichiers()