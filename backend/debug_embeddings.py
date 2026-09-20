# backend/debug_embeddings.py
import os
import numpy as np
from src.core.vector_store import VectorStore

def debug_embeddings():
    print("🐛 DIAGNOSTIC DES EMBEDDINGS ET RECHERCHE")
    print("=" * 60)
    
    store = VectorStore()
    
    print(f"📊 Documents dans le store: {len(store.documents)}")
    
    # 1. Analyse des documents indexés
    print("\n1. 📄 CONTENU DES DOCUMENTS INDEXÉS:")
    for i, doc in enumerate(store.documents):
        print(f"\n{i+1}. 📁 {doc['metadata']['file']}")
        print(f"   🏷️  Catégorie: {doc['metadata']['category']}")
        print(f"   🔑 Mots-clés: {doc['metadata']['keywords'][:3]}")
        print(f"   📝 Texte indexé: {doc['text'][:100]}...")
        print(f"   📏 Longueur embedding: {len(doc['embedding'])}")
    
    # 2. Test des similarités internes
    print("\n2. 🔍 TEST DES SIMILARITÉS INTERNES:")
    if store.embedder and len(store.documents) > 1:
        # Calculer les similarités entre tous les documents
        embeddings = np.array([doc['embedding'] for doc in store.documents])
        norms = np.linalg.norm(embeddings, axis=1)
        normalized_embeddings = embeddings / norms[:, np.newaxis]
        
        similarity_matrix = np.dot(normalized_embeddings, normalized_embeddings.T)
        
        print("   Matrice de similarité entre documents:")
        for i in range(len(store.documents)):
            for j in range(i+1, len(store.documents)):
                sim = similarity_matrix[i, j]
                doc1 = store.documents[i]['metadata']['file']
                doc2 = store.documents[j]['metadata']['file']
                print(f"   {doc1[:15]} ↔ {doc2[:15]} : {sim:.3f}")
    
    # 3. Test de recherche détaillé
    print("\n3. 🎯 TEST DÉTAILLÉ DES RECHERCHES:")
    test_queries = [
        "AI",
        "intelligence artificielle", 
        "femme",
        "test simple"
    ]
    
    for query in test_queries:
        print(f"\n   🔍 REQUÊTE: '{query}'")
        
        # Embedding de la requête
        if store.embedder:
            query_embedding = store.embedder.encode([query])[0]
            query_norm = np.linalg.norm(query_embedding)
            normalized_query = query_embedding / query_norm
        else:
            print("   ❌ Embedder non disponible")
            continue
        
        # Calcul manuel des similarités
        results = []
        for doc in store.documents:
            doc_embedding = np.array(doc['embedding'])
            doc_norm = np.linalg.norm(doc_embedding)
            
            if doc_norm > 0:
                normalized_doc = doc_embedding / doc_norm
                similarity = np.dot(normalized_query, normalized_doc)
            else:
                similarity = 0.0
                
            results.append((doc, similarity))
        
        # Trier par similarité
        results.sort(key=lambda x: x[1], reverse=True)
        
        print(f"   📈 Résultats (similarité cosinus):")
        for doc, sim in results[:3]:
            print(f"      📄 {doc['metadata']['file'][:20]}... : {sim:.3f}")
    
    # 4. Vérification FAISS
    print("\n4. 🔧 DIAGNOSTIC FAISS:")
    if store.index:
        print(f"   ✅ Index FAISS créé")
        print(f"   📐 Dimension: {store.index.d}")
        print(f"   📊 Total vecteurs: {store.index.ntotal}")
    else:
        print("   ❌ Index FAISS non créé")

if __name__ == "__main__":
    debug_embeddings()