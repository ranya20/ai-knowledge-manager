import os
import sys
import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.document_processor import DocumentProcessor
from src.core.qa_engine import QAEngine
from src.core.vector_store import VectorStore
import config

def test_complet_system():
    print("🧪 TEST COMPLET DU SYSTÈME RAG")
    print("=" * 60)
    
    # 1. ÉTAT INITIAL
    print("\n1. 📊 ÉTAT INITIAL DU SYSTÈME")
    vector_store = VectorStore(config.config)
    stats_initial = vector_store.get_stats()
    print(f"   - Documents dans vector_store: {stats_initial['total_documents']}")
    print(f"   - Fichiers uniques: {stats_initial['unique_files']}")
    
    # Compter les fichiers dans incoming
    fichiers_incoming = []
    if os.path.exists(config.config.INCOMING_DIR):
        fichiers_incoming = [f for f in os.listdir(config.config.INCOMING_DIR) 
                           if not f.startswith('.') and os.path.isfile(os.path.join(config.config.INCOMING_DIR, f))]
    
    print(f"   - Fichiers dans incoming/: {len(fichiers_incoming)}")
    for f in fichiers_incoming:
        print(f"     • {f}")
    
    # 2. TRAITEMENT DES FICHIERS
    print(f"\n2. 🔧 TRAITEMENT DES {len(fichiers_incoming)} FICHIERS")
    processor = DocumentProcessor(config.config)
    
    resultats_traitement = []
    for filename in fichiers_incoming:
        file_path = os.path.join(config.config.INCOMING_DIR, filename)
        print(f"\n   📄 Traitement de: {filename}")
        
        debut = time.time()
        resultat = processor.process_file(file_path)
        duree = time.time() - debut
        
        statut = "✅ SUCCÈS" if resultat.get('status') == 'success' else "❌ ÉCHEC"
        resultats_traitement.append((filename, statut, duree))
        
        print(f"      {statut} ({duree:.2f}s)")
        if resultat.get('error'):
            print(f"      Erreur: {resultat.get('error')}")
        if resultat.get('rag_processed'):
            print(f"      RAG: ✅ Traité")
    
    # 3. ÉTAT APRÈS TRAITEMENT
    print(f"\n3. 📊 ÉTAT APRÈS TRAITEMENT")
    stats_final = vector_store.get_stats()
    print(f"   - Documents dans vector_store: {stats_final['total_documents']}")
    print(f"   - Fichiers uniques: {stats_final['unique_files']}")
    print(f"   - Nouveaux documents ajoutés: {stats_final['total_documents'] - stats_initial['total_documents']}")
    
    # Vérifier le déplacement des fichiers
    print(f"\n4. 📁 VÉRIFICATION DÉPLACEMENT FICHIERS")
    fichiers_incoming_apres = os.listdir(config.config.INCOMING_DIR) if os.path.exists(config.config.INCOMING_DIR) else []
    fichiers_processed = os.listdir(config.config.PROCESSED_DIR) if os.path.exists(config.config.PROCESSED_DIR) else []
    fichiers_failed = os.listdir(config.config.FAILED_DIR) if os.path.exists(config.config.FAILED_DIR) else []
    
    print(f"   - Fichiers dans incoming/: {len(fichiers_incoming_apres)}")
    print(f"   - Fichiers dans processed/: {len(fichiers_processed)}")
    print(f"   - Fichiers dans failed/: {len(fichiers_failed)}")
    
    # 5. TEST QUESTIONS-RÉPONSES
    print(f"\n5. ❓ TEST QUESTIONS-RÉPONSES")
    qa_engine = QAEngine(config.config)
    
    questions_test = [
        "De quoi parlent les documents sur les technologies?",
        "Quel est l'objectif du projet RAG?",
        "Quelles technologies émergentes sont mentionnées?",
        "Quel est le statut du projet?",
        "Quels formats de documents sont supportés?"
    ]
    
    for i, question in enumerate(questions_test, 1):
        print(f"\n   {i}. Q: {question}")
        try:
            debut = time.time()
            resultat = qa_engine.ask_question(question)
            duree = time.time() - debut
            
            print(f"      A: {resultat['answer'][:100]}...")
            print(f"      📚 Sources: {resultat['source_files']}")
            print(f"      ⏱️  Temps: {duree:.2f}s")
            print(f"      🔍 Documents utilisés: {resultat['search_stats']['documents_after_filter']}")
            
        except Exception as e:
            print(f"      ❌ Erreur: {e}")
    
    # 6. RÉSUMÉ FINAL
    print(f"\n6. 📈 RÉSUMÉ FINAL")
    print(f"   - Fichiers traités: {len(resultats_traitement)}")
    succes = sum(1 for _, statut, _ in resultats_traitement if "✅" in statut)
    echecs = len(resultats_traitement) - succes
    print(f"   - ✅ Succès: {succes}")
    print(f"   - ❌ Échecs: {echecs}")
    
    temps_total = sum(duree for _, _, duree in resultats_traitement)
    print(f"   - ⏱️  Temps total traitement: {temps_total:.2f}s")
    
    if echecs == 0:
        print(f"\n🎉 TOUS LES TESTS ONT RÉUSSI !")
    else:
        print(f"\n⚠️  {echecs} test(s) ont échoué")

if __name__ == "__main__":
    test_complet_system()