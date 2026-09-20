import os
import json
from typing import List, Dict, Any
from .vector_store import VectorStore
from .llm_integration import LLMIntegration

class QAEngine:
    """Moteur de questions/réponses avec RAG"""
    
    def __init__(self, config):
        self.config = config
        self.vector_store = VectorStore(config)
        self.llm = LLMIntegration(config)
        print("✅ QAEngine initialisé")
    
    def ask_question(self, question: str, use_llm: bool = True, top_k: int = 5, similarity_threshold: float = None) -> Dict[str, Any]:
        """
        Pose une question et retourne une réponse contextuelle
        
        Args:
            question: La question de l'utilisateur
            use_llm: Utiliser LLM pour la réponse (sinon réponse basique)
            top_k: Nombre de documents similaires à récupérer
            similarity_threshold: Seuil de similarité personnalisé (optionnel)
        """
        if similarity_threshold is None:
            similarity_threshold = self.config.SIMILARITY_THRESHOLD
            
        print(f"🔍 Recherche de documents pour: '{question}' (seuil: {similarity_threshold})")
        
        # Recherche de documents similaires
        similar_docs = self.vector_store.search_similar(question, top_k=top_k, similarity_threshold=similarity_threshold)
        
        # Filtrer par seuil de similarité (double vérification)
        relevant_docs = [
            doc for doc in similar_docs 
            if doc['similarity_score'] >= similarity_threshold
        ]
        
        print(f"📄 Documents pertinents trouvés: {len(relevant_docs)}")
        
        # Génération de la réponse
        if use_llm and relevant_docs:
            answer = self.llm.generate_rag_response(question, relevant_docs)
        else:
            answer = self._generate_fallback_answer(question, relevant_docs)
        
        # Préparation des résultats
        source_files = list(set(
            doc['metadata'].get('file_name', 'Inconnu') for doc in relevant_docs
        ))
        
        return {
            'question': question,
            'answer': answer,
            'relevant_documents': relevant_docs,
            'source_files': source_files,
            'total_sources': len(source_files),
            'used_llm': use_llm,
            'search_stats': {
                'documents_found': len(similar_docs),
                'documents_after_filter': len(relevant_docs),
                'similarity_threshold': similarity_threshold
            }
        }
    
    def _generate_fallback_answer(self, question: str, relevant_docs: List[Dict]) -> str:
        """Génère une réponse basique si LLM n'est pas utilisé"""
        if not relevant_docs:
            return "Je n'ai pas trouvé d'informations pertinentes dans vos documents pour répondre à cette question."
        
        # Réponse basée sur le contenu le plus similaire
        most_relevant = relevant_docs[0]
        content = most_relevant['content']
        source = most_relevant['metadata'].get('file_name', 'Document inconnu')
        
        # Extraire la partie la plus pertinente
        excerpt = content[:500] + "..." if len(content) > 500 else content
        
        return f"D'après le document '{source}':\n\n{excerpt}"
    
    def search_files_by_topic(self, topic: str, similarity_threshold: float = 0.3) -> List[Dict[str, Any]]:
        """Trouve tous les fichiers qui parlent d'un sujet spécifique"""
        results = self.ask_question(
            f"Quels documents parlent de {topic} ?", 
            use_llm=False, 
            top_k=10,
            similarity_threshold=similarity_threshold
        )
        
        # Organiser les résultats par fichier
        file_scores = {}
        for doc in results['relevant_documents']:
            file_name = doc['metadata'].get('file_name', 'Inconnu')
            score = doc['similarity_score']
            
            if file_name not in file_scores or score > file_scores[file_name]['score']:
                file_scores[file_name] = {
                    'file_name': file_name,
                    'file_path': doc['metadata'].get('file_path', ''),
                    'score': score,
                    'excerpt': doc['content'][:200] + "..." if len(doc['content']) > 200 else doc['content']
                }
        
        return sorted(file_scores.values(), key=lambda x: x['score'], reverse=True)
    
    def get_document_relationships(self, document_name: str) -> List[Dict[str, Any]]:
        """Trouve les documents liés à un document spécifique"""
        # CORRECTION: Accès correct aux métadonnées
        target_doc = None
        for doc in self.vector_store.documents:
            metadata = doc.get('metadata', {})
            if metadata.get('file_name') == document_name and not metadata.get('is_chunk', False):
                target_doc = doc
                break
        
        if not target_doc:
            print(f"❌ Document '{document_name}' non trouvé")
            return []
        
        # Rechercher des documents similaires au contenu du document cible
        target_content = target_doc.get('text', '')  # CORRECTION: 'text' au lieu de 'content'
        similar_docs = self.vector_store.search_similar(target_content, top_k=10, similarity_threshold=0.3)
        
        related_docs = []
        for doc in similar_docs:
            doc_metadata = doc['metadata']
            if doc_metadata.get('file_name') != document_name:  # Exclure le document lui-même
                related_docs.append({
                    'file_name': doc_metadata.get('file_name', 'Inconnu'),
                    'file_path': doc_metadata.get('file_path', ''),
                    'similarity_score': doc['similarity_score'],
                    'relationship': self._get_relationship_label(doc['similarity_score'])
                })
        
        return sorted(related_docs, key=lambda x: x['similarity_score'], reverse=True)
    
    def _get_relationship_label(self, similarity: float) -> str:
        """Convertit un score de similarité en label de relation"""
        if similarity > 0.8:
            return "très similaire"
        elif similarity > 0.6:
            return "similaire"
        elif similarity > 0.4:
            return "lié"
        else:
            return "faiblement lié"
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques du système"""
        vector_stats = self.vector_store.get_stats()
        return {
            'vector_store': vector_stats,
            'llm_provider': self.config.LLM_PROVIDER,
            'similarity_threshold': self.config.SIMILARITY_THRESHOLD,
            'chunk_size': self.config.CHUNK_SIZE
        }
    
    def debug_vector_store(self) -> Dict[str, Any]:
        """Fonction de debug pour inspecter le vector store"""
        print("🔍 DEBUG VECTOR STORE")
        
        stats = self.vector_store.get_stats()
        debug_info = {
            'total_documents': stats['total_documents'],
            'documents_sample': []
        }
        
        # Afficher un échantillon des documents
        for i, doc in enumerate(self.vector_store.documents[:5]):
            debug_info['documents_sample'].append({
                'index': i,
                'id': doc.get('id', 'N/A'),
                'metadata': doc.get('metadata', {}),
                'text_preview': doc.get('text', 'N/A')[:100] + '...' if doc.get('text') else 'N/A'
            })
        
        # Test de recherche avec différents seuils
        test_queries = ["test", "document", "ia", "intelligence"]
        debug_info['search_tests'] = {}
        
        for query in test_queries:
            debug_info['search_tests'][query] = {}
            for threshold in [0.7, 0.5, 0.3, 0.1]:
                results = self.vector_store.search_similar(query, top_k=3, similarity_threshold=threshold)
                debug_info['search_tests'][query][threshold] = len(results)
        
        return debug_info

# Test du module
if __name__ == "__main__":
    # Configuration de test
    class TestConfig:
        VECTOR_STORE_PATH = "data/vector_store_test"
        EMBEDDING_MODEL = "all-MiniLM-L6-v2"
        EMBEDDING_DIMENSION = 384
        CHUNK_SIZE = 1000
        CHUNK_OVERLAP = 100
        SIMILARITY_THRESHOLD = 0.3  # Seuil bas pour les tests
        LLM_PROVIDER = "openrouter"
        OPENROUTER_API_KEY = "test_key"
        OPENROUTER_MODEL = "mistralai/mistral-7b-instruct"
    
    try:
        config = TestConfig()
        qa_engine = QAEngine(config)
        
        print("🧪 Test QAEngine...")
        
        # Test des statistiques
        stats = qa_engine.get_system_stats()
        print(f"✅ Statistiques: {stats['vector_store']['total_documents']} documents")
        
        # Test de debug
        debug_info = qa_engine.debug_vector_store()
        print(f"🔍 Debug: {debug_info['total_documents']} documents au total")
        
        # Test de recherche simple
        if debug_info['total_documents'] > 0:
            result = qa_engine.ask_question("test", use_llm=False, similarity_threshold=0.1)
            print(f"🔍 Recherche test: {len(result['relevant_documents'])} résultats")
        
        print("✅ QAEngine test réussi")
        
    except Exception as e:
        print(f"❌ Erreur QAEngine: {e}")
        import traceback
        traceback.print_exc()