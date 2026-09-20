import numpy as np
import faiss
import json
import os
from typing import List, Dict, Any, Optional
from sentence_transformers import SentenceTransformer

class VectorStore:
    def __init__(self, config):
        """
        Initialise le vector store avec configuration
        
        Args:
            config: Objet de configuration avec VECTOR_STORE_PATH, EMBEDDING_MODEL, etc.
        """
        self.config = config
        self.storage_path = config.VECTOR_STORE_PATH
        self.index = None
        self.documents = []
        self.embedder = None
        self._initialize_store()
        self._load_embedder()
    
    def _load_embedder(self):
        """Charge le modèle d'embedding SentenceTransformers"""
        try:
            self.embedder = SentenceTransformer(self.config.EMBEDDING_MODEL)
            print(f"✅ Embedding model chargé: {self.config.EMBEDDING_MODEL}")
        except Exception as e:
            print(f"❌ Erreur chargement embedding: {e}")
            self.embedder = None
    
    def _initialize_store(self):
        """Initialise ou charge le store vectoriel"""
        os.makedirs(self.storage_path, exist_ok=True)
        
        # CORRECTION : Utiliser "faiss_index" au lieu de "faiss.index"
        index_path = os.path.join(self.storage_path, "faiss_index")
        docs_path = os.path.join(self.storage_path, "documents.json")
        
        if os.path.exists(index_path) and os.path.exists(docs_path):
            self._load_existing_store(index_path, docs_path)
        else:
            self._create_new_store()
    
    def add_document(self, text: str, metadata: Dict[str, Any]) -> bool:
        """
        Ajoute un document au vector store avec chunking automatique
        
        Args:
            text: Texte du document
            metadata: Métadonnées du document
        """
        if not text or len(text.strip()) < 10:
            print("⚠️  Texte trop court, ignoré")
            return False
        
        try:
            # Découper le texte en chunks si nécessaire
            if len(text) > self.config.CHUNK_SIZE:
                chunks = self._chunk_text(text)
                success_count = 0
                
                for i, chunk in enumerate(chunks):
                    chunk_metadata = metadata.copy()
                    chunk_metadata.update({
                        'chunk_id': i,
                        'chunk_content': chunk,
                        'is_chunk': True,
                        'total_chunks': len(chunks)
                    })
                    
                    if self._add_single_chunk(chunk, chunk_metadata):
                        success_count += 1
                
                print(f"✅ Document chunké ajouté: {metadata.get('file_name', 'Inconnu')} - {success_count}/{len(chunks)} chunks")
                return success_count > 0
            else:
                # Document complet (sans chunking)
                full_metadata = metadata.copy()
                full_metadata.update({
                    'content': text,
                    'is_chunk': False
                })
                return self._add_single_chunk(text, full_metadata)
            
        except Exception as e:
            print(f"❌ Erreur ajout document: {e}")
            return False
    
    def _add_single_chunk(self, text: str, metadata: Dict[str, Any]) -> bool:
        """Ajoute un chunk individuel au vector store"""
        try:
            # Générer l'embedding
            if self.embedder:
                embedding = self.embedder.encode([text])[0]
            else:
                embedding = self._simple_embedding(text)
            
            # Préparer le document
            doc_id = f"doc_{len(self.documents)}"
            document = {
                "id": doc_id,
                "text": text,
                "metadata": metadata,
                "embedding": embedding.tolist() if hasattr(embedding, 'tolist') else embedding
            }
            
            # Ajouter à l'index FAISS
            if self.index is None:
                self._create_index(embedding)
            else:
                embedding_array = np.array([embedding]).astype('float32')
                self.index.add(embedding_array)
            
            self.documents.append(document)
            
            # ✅ CORRECTION : SAUVEGARDER IMMÉDIATEMENT APRÈS CHAQUE AJOUT
            self._save_store()
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur ajout chunk: {e}")
            return False
    
    def _chunk_text(self, text: str) -> List[str]:
        """Découpe le texte en chunks avec chevauchement"""
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + self.config.CHUNK_SIZE
            
            # Essayer de couper à la fin d'une phrase
            if end < len(text):
                last_period = text.rfind('. ', start, end)
                if last_period != -1 and last_period > start + (self.config.CHUNK_SIZE // 2):
                    end = last_period + 1
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            start = end - self.config.CHUNK_OVERLAP
        
        return chunks
    
    def search_similar(self, query: str, top_k: int = 5, similarity_threshold: float = None) -> List[Dict[str, Any]]:
        """
        Recherche sémantique avec filtrage par similarité
        
        Args:
            query: Requête de recherche
            top_k: Nombre de résultats à retourner
            similarity_threshold: Seuil de similarité (utilise config par défaut)
        """
        if self.index is None or not self.documents:
            return []
        
        if similarity_threshold is None:
            similarity_threshold = self.config.SIMILARITY_THRESHOLD
        
        try:
            # Embedding de la requête
            if self.embedder:
                query_embedding = self.embedder.encode([query])[0]
            else:
                query_embedding = np.array(self._simple_embedding(query))
            
            # Recherche FAISS
            k_search = min(top_k * 2, len(self.documents))
            query_array = np.array([query_embedding]).astype('float32')
            
            # Utiliser IndexFlatIP pour similarité cosinus
            distances, indices = self.index.search(query_array, k_search)
            
            # Formater les résultats
            results = []
            for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
                if 0 <= idx < len(self.documents):
                    # Conversion pour IndexFlatIP (produit scalaire → similarité cosinus)
                    similarity = float(distance)  # Déjà normalisé pour IndexFlatIP
                    
                    if similarity >= similarity_threshold:
                        doc = self.documents[idx]
                        results.append({
                            'document': doc,
                            'similarity_score': round(similarity, 3),
                            'content': doc['text'],
                            'metadata': doc['metadata']
                        })
                    
                    if len(results) >= top_k:
                        break
            
            # Trier par similarité décroissante
            results.sort(key=lambda x: x['similarity_score'], reverse=True)
            
            print(f"🔍 '{query[:50]}...' → {len(results)} résultats (seuil: {similarity_threshold})")
            return results
            
        except Exception as e:
            print(f"❌ Erreur recherche: {e}")
            return []
    
    def semantic_search(self, query: str, k: int = 5) -> List[Dict]:
        """Alias pour compatibilité avec l'ancien code"""
        return self.search_similar(query, k)
    
    def _simple_embedding(self, text: str) -> List[float]:
        """Embedding simple de fallback (moins bon mais fonctionnel)"""
        # Utiliser une dimension standard
        dimension = self.config.EMBEDDING_DIMENSION
        words = text.lower().split()
        embedding = [0.0] * dimension
        
        for i, word in enumerate(words[:dimension]):
            if word:
                # Hash simple mais déterministe
                embedding[i] = (hash(word) % 100) / 100.0
        
        return embedding
    
    def _create_index(self, first_embedding: List[float]):
        """Crée un nouvel index FAISS avec IndexFlatIP pour similarité cosinus"""
        dimension = len(first_embedding)
        self.index = faiss.IndexFlatIP(dimension)  # Produit scalaire pour similarité cosinus
        
        # Normaliser le premier embedding
        embedding_np = np.array([first_embedding]).astype('float32')
        faiss.normalize_L2(embedding_np)
        self.index.add(embedding_np)
        
        print(f"🆕 Index FAISS IP créé (dimension: {dimension})")
    
    def _load_existing_store(self, index_path: str, docs_path: str):
        """Charge un store existant"""
        try:
            self.index = faiss.read_index(index_path)
            with open(docs_path, 'r', encoding='utf-8') as f:
                self.documents = json.load(f)
            print(f"✅ Vector store chargé: {len(self.documents)} documents")
        except Exception as e:
            print(f"❌ Erreur chargement store: {e}")
            self._create_new_store()
    
    def _save_store(self):
        """Sauvegarde le store sur disque"""
        try:
            if self.index is not None:
                # CORRECTION : Utiliser "faiss_index" au lieu de "faiss.index"
                index_path = os.path.join(self.storage_path, "faiss_index")
                faiss.write_index(self.index, index_path)
            
            docs_path = os.path.join(self.storage_path, "documents.json")
            with open(docs_path, 'w', encoding='utf-8') as f:
                json.dump(self.documents, f, ensure_ascii=False, indent=2)
                
            print(f"💾 Vector store sauvegardé: {len(self.documents)} documents")
                
        except Exception as e:
            print(f"⚠️  Erreur sauvegarde store: {e}")
    
    def _create_new_store(self):
        """Crée un nouveau store vide"""
        self.index = None
        self.documents = []
        print("🆕 Nouveau vector store créé")
    
    def get_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques du vector store"""
        total_docs = len(self.documents)
        chunks = [d for d in self.documents if d.get('metadata', {}).get('is_chunk', False)]
        full_docs = [d for d in self.documents if not d.get('metadata', {}).get('is_chunk', False)]
        
        return {
            'total_documents': total_docs,
            'total_embeddings': self.index.ntotal if self.index else 0,
            'embedding_dimension': self.index.d if self.index else 0,
            'documents_with_chunks': len(chunks),
            'full_documents': len(full_docs),
            'unique_files': len(set(
                d['metadata'].get('file_name', 'Unknown') 
                for d in self.documents
            ))
        }
    
    def clear_store(self):
        """Vide complètement le vector store"""
        self.index = None
        self.documents = []
        self._create_new_store()
        
        # Supprimer les fichiers
        index_path = os.path.join(self.storage_path, "faiss_index")  # CORRECTION
        docs_path = os.path.join(self.storage_path, "documents.json")
        
        for path in [index_path, docs_path]:
            if os.path.exists(path):
                os.remove(path)
        
        print("🗑️  Vector store vidé")
    
    def get_document_by_id(self, doc_id: str) -> Optional[Dict]:
        """Récupère un document par son ID"""
        for doc in self.documents:
            if doc.get('id') == doc_id:
                return doc
        return None
    
    def get_documents_by_filename(self, filename: str) -> List[Dict]:
        """Récupère tous les documents/chunks d'un fichier spécifique"""
        return [
            doc for doc in self.documents 
            if doc.get('metadata', {}).get('file_name') == filename
        ]
    
    def search_by_metadata(self, metadata_filter: Dict[str, Any]) -> List[Dict]:
        """Recherche par filtrage des métadonnées"""
        results = []
        for doc in self.documents:
            metadata = doc.get('metadata', {})
            match = True
            
            for key, value in metadata_filter.items():
                if metadata.get(key) != value:
                    match = False
                    break
            
            if match:
                results.append(doc)
        
        return results

# Test du module
if __name__ == "__main__":
    print("🧪 Test du Vector Store...")
    
    # Configuration de test
    class TestConfig:
        VECTOR_STORE_PATH = "data/vector_store_test"
        EMBEDDING_MODEL = "all-MiniLM-L6-v2"
        EMBEDDING_DIMENSION = 384
        CHUNK_SIZE = 500
        CHUNK_OVERLAP = 50
        SIMILARITY_THRESHOLD = 0.7
    
    try:
        config = TestConfig()
        store = VectorStore(config)
        
        # Test d'ajout
        test_text = "L'intelligence artificielle est un domaine passionnant de l'informatique."
        test_metadata = {
            "file_name": "test_document.txt",
            "file_type": ".txt",
            "source": "test"
        }
        
        success = store.add_document(test_text, test_metadata)
        print(f"✅ Ajout document: {success}")
        
        # Test de recherche
        results = store.search_similar("intelligence artificielle", top_k=3)
        print(f"✅ Résultats recherche: {len(results)}")
        
        # Test statistiques
        stats = store.get_stats()
        print(f"✅ Statistiques: {stats}")
        
    except Exception as e:
        print(f"❌ Erreur test: {e}")
        import traceback
        traceback.print_exc()