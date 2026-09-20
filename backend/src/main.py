# backend/src/main.py - VERSION COMPLÈTE AVEC INTELLIGENCE
import sys
import os
import time
import json
from datetime import datetime

# Chemin absolu vers backend
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

try:
    # Import absolu depuis le dossier backend
    from config import Config
    from src.file_monitor.organizer import FileOrganizer
    from src.core.document_processor import DocumentProcessor
    from src.models.nlp_processor import NLPProcessor
    from src.core.vector_store import VectorStore
    print("✅ Tous les imports réussis dans main.py")
except ImportError as e:
    print(f"❌ Erreur import dans main.py: {e}")
    print("💡 Assure-toi que tous les modules sont créés:")
    print("   - src/models/nlp_processor.py")
    print("   - src/core/vector_store.py")
    raise

class KnowledgeManager:
    def __init__(self):
        self.config = Config()
        self.organizer = FileOrganizer(self.config)
        self.processor = DocumentProcessor(self.config)
        
        # ✅ NOUVEAU : Initialisation des composants intelligents
        self.nlp_processor = NLPProcessor(use_advanced_models=False)  # Mode offline
        self.vector_store = VectorStore()
        
        print("✅ AI Knowledge Manager intelligent initialisé!")
        print(f"   📁 Surveillance: {self.config.INCOMING_DIR}")
        print(f"   🧠 NLP: {'Activé' if hasattr(self, 'nlp_processor') else 'Désactivé'}")
        print(f"   🔍 Recherche: {'Activé' if hasattr(self, 'vector_store') else 'Désactivé'}")
        
    def run_once(self):
        """Exécute un cycle de traitement intelligent"""
        new_files = self.organizer.get_new_files()
        
        if not new_files:
            print("⏳ Aucun nouveau fichier à traiter")
            return 0
        
        processed_count = 0
        
        for filename in new_files:
            try:
                print(f"\n🎯 Traitement intelligent de: {filename}")
                
                # Étape 1: Déplacer vers processing
                processing_path = self.organizer.move_to_processing(filename)
                
                # Étape 2: Traitement du document (PDF/OCR)
                result = self.processor.process_file(processing_path)
                
                # Étape 3: Si succès, analyse NLP intelligente
                if result['status'] == 'success':
                    self._process_with_intelligence(filename, result)
                    self.organizer.move_to_processed(filename, success=True)
                    processed_count += 1
                    print(f"✅ Succès intelligent: {filename}")
                else:
                    self.organizer.move_to_processed(filename, success=False)
                    print(f"❌ Erreur: {filename} - {result['error']}")
                    
            except Exception as e:
                print(f"💥 Erreur critique avec {filename}: {e}")
                self.organizer.move_to_processed(filename, success=False)
        
        return processed_count
    
    def _process_with_intelligence(self, filename: str, result: dict):
        """Traite le document avec analyse NLP intelligente"""
        try:
            # ✅ NOUVEAU : Analyse NLP avancée
            nlp_analysis = self.nlp_processor.analyze_document(
                result.get('clean_text', ''),
                filename,  # Utilise le nom du fichier comme titre
                result.get('metadata', {}).get('pdf_type', '')  # Type de document
            )
            
            # Sauvegarde des résultats enrichis
            self._save_intelligent_results(filename, result, nlp_analysis)
            
            # Ajout au vector store pour recherche sémantique
            if nlp_analysis['analysis_success']:
                self._add_to_vector_store(filename, result, nlp_analysis)
                
        except Exception as e:
            print(f"⚠️  Erreur analyse intelligente: {e}")
            # Fallback: sauvegarde basique sans NLP
            self._save_results_basic(filename, result)
    
    def _save_intelligent_results(self, filename: str, processing_result: dict, nlp_analysis: dict):
        """Sauvegarde les résultats avec analyse intelligente"""
        base_name = os.path.splitext(filename)[0]
        output_path = os.path.join(
            self.config.PROCESSED_DIR, 
            f"{base_name}.json"
        )
        
        output_data = {
            'original_file': filename,
            'processed_at': datetime.now().isoformat(),
            'metadata': processing_result.get('metadata', {}),
            'clean_text': processing_result.get('clean_text', ''),
            'raw_text': processing_result.get('raw_text', ''),
            # ✅ NOUVEAU : Analyse intelligente
            'nlp_analysis': nlp_analysis
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Résultats intelligents sauvegardés: {output_path}")
        
        # Affichage des insights
        if nlp_analysis['analysis_success']:
            print(f"   📝 Résumé: {nlp_analysis['summary'][:80]}...")
            print(f"   🔑 Mots-clés: {', '.join(nlp_analysis['keywords'][:5])}")
            print(f"   🏷️ Catégorie: {nlp_analysis['category']} (confiance: {nlp_analysis['category_confidence']:.2f})")
            print(f"   📊 Qualité: {nlp_analysis['quality_score']:.2f}")
    
    def _add_to_vector_store(self, filename: str, processing_result: dict, nlp_analysis: dict):
        """Ajoute le document au vector store pour recherche"""
        try:
            base_name = os.path.splitext(filename)[0]
            
            success = self.vector_store.add_document(
                text=processing_result.get('clean_text', ''),
                metadata={
                    'file': filename,
                    'category': nlp_analysis['category'],
                    'keywords': nlp_analysis['keywords'],
                    'summary': nlp_analysis['summary'],
                    'quality_score': nlp_analysis['quality_score'],
                    'processed_at': datetime.now().isoformat()
                },
                document_id=base_name
            )
            
            if success:
                print(f"🔍 Document ajouté à la recherche sémantique: {filename}")
            else:
                print(f"⚠️  Impossible d'ajouter à la recherche: {filename}")
                
        except Exception as e:
            print(f"⚠️  Erreur vector store: {e}")
    
    def _save_results_basic(self, filename: str, result: dict):
        """Sauvegarde basique (fallback)"""
        base_name = os.path.splitext(filename)[0]
        output_path = os.path.join(
            self.config.PROCESSED_DIR, 
            f"{base_name}.json"
        )
        
        output_data = {
            'original_file': filename,
            'processed_at': datetime.now().isoformat(),
            'metadata': result.get('metadata', {}),
            'clean_text': result.get('clean_text', ''),
            'raw_text': result.get('raw_text', '')
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        print(f"💾 Résultats basiques sauvegardés: {output_path}")
    
    def semantic_search(self, query: str, k: int = 5):
        """Recherche sémantique dans les documents"""
        if not hasattr(self, 'vector_store'):
            print("❌ Vector store non initialisé")
            return []
        
        try:
            results = self.vector_store.semantic_search(query, k)
            print(f"🔍 Recherche: '{query}' → {len(results)} résultats")
            return results
        except Exception as e:
            print(f"❌ Erreur recherche: {e}")
            return []
    
    def get_document_count(self):
        """Retourne le nombre de documents indexés"""
        if hasattr(self, 'vector_store') and hasattr(self.vector_store, 'documents'):
            return len(self.vector_store.documents)
        return 
    
    def run_continuous(self, interval=10):
        """Exécute en continu avec un intervalle"""
        print("🔍 Surveillance du dossier: data/incoming/")
        print("⏰ Vérification toutes les 10 secondes")
        print("🛑 Ctrl+C pour arrêter")
        print("🧠 Mode intelligent activé")
        print("─" * 50)
        
        try:
            cycle_count = 0
            while True:
                processed = self.run_once()
                cycle_count += 1
                
                if processed > 0:
                    print(f"📊 Cycle {cycle_count}: {processed} fichier(s) traité(s)")
                    total_docs = self.get_document_count()
                    if total_docs > 0:
                        print(f"📚 Total documents indexés: {total_docs}")
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n🛑 Arrêt demandé par l'utilisateur")
            total_docs = self.get_document_count()
            if total_docs > 0:
                print(f"📚 Session terminée - {total_docs} documents indexés")
        except Exception as e:
            print(f"💥 Erreur inattendue: {e}")

# ✅ NOUVEAU : Interface de recherche en ligne de commande
def interactive_search(manager):
    """Mode recherche interactif"""
    print("\n🎯 Mode Recherche Interactive")
    print("Tape 'quit' pour revenir au mode surveillance")
    
    while True:
        try:
            query = input("\n🔍 Recherche: ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("Retour au mode surveillance...")
                break
            
            if not query:
                continue
            
            # Recherche sémantique
            results = manager.semantic_search(query, k=3)
            
            if results:
                print(f"📄 {len(results)} résultats trouvés:")
                for i, result in enumerate(results, 1):
                    doc = result['document']
                    similarity = result['similarity']
                    
                    print(f"\n{i}. 📁 {doc['metadata']['file']}")
                    print(f"   🏷️  Catégorie: {doc['metadata']['category']}")
                    print(f"   📊 Similarité: {similarity:.2f}")
                    print(f"   📝 {doc['metadata']['summary'][:100]}...")
                    print(f"   🔑 Mots-clés: {', '.join(doc['metadata']['keywords'][:3])}")
            else:
                print("❌ Aucun résultat trouvé")
                
        except KeyboardInterrupt:
            print("\nRetour au mode surveillance...")
            break
        except Exception as e:
            print(f"❌ Erreur recherche: {e}")

# ✅ NOUVEAU : Mode avec options
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='AI Knowledge Manager')
    parser.add_argument('--search', action='store_true', help='Mode recherche interactive')
    parser.add_argument('--query', type=str, help='Recherche spécifique')
    parser.add_argument('--once', action='store_true', help='Exécuter une seule fois')
    
    args = parser.parse_args()
    
    print("🚀 AI Knowledge Manager - Démarrage...")
    manager = KnowledgeManager()
    
    if args.search:
        # Mode recherche interactive
        interactive_search(manager)
    elif args.query:
        # Recherche spécifique
        results = manager.semantic_search(args.query, k=5)
        if results:
            print(f"🔍 Résultats pour '{args.query}':")
            for i, result in enumerate(results, 1):
                doc = result['document']
                print(f"{i}. {doc['metadata']['file']} (similarité: {result['similarity']:.2f})")
        else:
            print("❌ Aucun résultat")
    elif args.once:
        # Exécution unique
        print("🔍 Exécution unique...")
        processed = manager.run_once()
        print(f"📊 Traitement terminé: {processed} fichier(s)")
    else:
        # Mode surveillance continu (par défaut)
        manager.run_continuous()