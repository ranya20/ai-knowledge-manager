from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys

# Ajouter le chemin pour les imports
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from src.core.qa_engine import QAEngine
from src.core.document_processor import DocumentProcessor
from src.core.vector_store import VectorStore
from src.core.url_processor import URLProcessor
from src.core.llm_integration import LLMIntegration
import config

app = Flask(__name__)
CORS(app)

print("🚀 Initialisation du système RAG...")

# ✅ CORRECTION : NE PAS initialiser les composants ici
# On va les créer à CHAQUE requête pour avoir les données fraîches

def get_fresh_qa_engine():
    """Crée une NOUVELLE instance de QAEngine avec les données fraîches"""
    print("🔄 Création d'un nouveau QAEngine avec données fraîches...")
    return QAEngine(config.config)

def get_fresh_document_processor():
    """Crée une NOUVELLE instance de DocumentProcessor"""
    return DocumentProcessor(config.config)

def get_fresh_vector_store():
    """Crée une NOUVELLE instance de VectorStore"""
    return VectorStore(config.config)

def get_fresh_url_processor():
    """Crée une NOUVELLE instance de URLProcessor"""
    llm = LLMIntegration(config.config)
    return URLProcessor(config.config, llm)

@app.route('/api/ask', methods=['POST'])
def ask_question():
    """Endpoint pour poser des questions"""
    try:
        data = request.json
        question = data.get('question', '')
        
        if not question:
            return jsonify({'error': 'Question requise'}), 400
        
        print(f"❓ Question reçue: {question}")
        
        # ✅ CORRECTION : CRÉER UNE NOUVELLE INSTANCE À CHAQUE FOIS
        qa_engine = get_fresh_qa_engine()
        result = qa_engine.ask_question(question)
        
        return jsonify({
            'answer': result['answer'],
            'sources': result['source_files'],
            'search_stats': result['search_stats']
        })
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Endpoint pour uploader des fichiers"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Aucun fichier'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Nom de fichier vide'}), 400
        
        print(f"📁 Upload fichier: {file.filename}")
        
        # Sauvegarder temporairement le fichier
        temp_path = os.path.join(config.config.INCOMING_DIR, file.filename)
        file.save(temp_path)
        
        # ✅ CORRECTION : UTILISER UNE NOUVELLE INSTANCE
        document_processor = get_fresh_document_processor()
        result = document_processor.process_file(temp_path)
        
        if result.get('status') == 'success':
            return jsonify({
                'success': True,
                'filename': file.filename,
                'message': 'Fichier traité avec succès',
                'result': result
            })
        else:
            return jsonify({
                'success': False,
                'error': result.get('error', 'Erreur inconnue')
            }), 400
            
    except Exception as e:
        print(f"❌ Erreur upload: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/process-url', methods=['POST'])
def process_url():
    """NOUVEL ENDPOINT : Traite une URL et répond immédiatement dans le chat"""
    try:
        data = request.json
        url = data.get('url', '')
        question = data.get('question', '')
        
        if not url:
            return jsonify({'error': 'URL requise'}), 400
        
        print(f"🌐 Traitement URL: {url}")
        if question:
            print(f"   📝 Question associée: {question}")
        
        # ✅ CRÉER UNE NOUVELLE INSTANCE
        url_processor = get_fresh_url_processor()
        result = url_processor.process_url_for_chat(url, question)
        
        if result['success']:
            return jsonify({
                'success': True,
                'url': url,
                'response': result['response'],
                'summary': result.get('summary', ''),
                'keywords': result.get('keywords', []),
                'content_length': result.get('content_length', 0)
            })
        else:
            return jsonify({
                'success': False,
                'error': result.get('error', 'Erreur inconnue'),
                'url': url
            }), 400
            
    except Exception as e:
        print(f"❌ Erreur traitement URL: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/add-url', methods=['POST'])
def add_url():
    """NOUVEL ENDPOINT : Ajoute une URL à la base de connaissances"""
    try:
        data = request.json
        url = data.get('url', '')
        
        if not url:
            return jsonify({'error': 'URL requise'}), 400
        
        print(f"🌐 Ajout URL à la base: {url}")
        
        # ✅ CRÉER UNE NOUVELLE INSTANCE
        url_processor = get_fresh_url_processor()
        
        # Extraire le contenu
        extraction_result = url_processor.extract_content(url)
        
        if not extraction_result['success']:
            return jsonify({
                'success': False,
                'error': extraction_result.get('error', 'Erreur extraction'),
                'url': url
            }), 400
        
        # Sauvegarder dans un fichier
        file_path = url_processor.save_url_to_file(url, extraction_result['content'])
        
        if file_path:
            # Traiter le fichier via le pipeline existant
            document_processor = get_fresh_document_processor()
            processing_result = document_processor.process_file(file_path)
            
            if processing_result.get('status') == 'success':
                return jsonify({
                    'success': True,
                    'url': url,
                    'filename': os.path.basename(file_path),
                    'message': 'URL ajoutée à la base de connaissances',
                    'extraction_result': extraction_result,
                    'processing_result': processing_result
                })
            else:
                return jsonify({
                    'success': False,
                    'error': processing_result.get('error', 'Erreur traitement fichier'),
                    'url': url
                }), 400
        else:
            return jsonify({
                'success': False,
                'error': 'Erreur sauvegarde du fichier',
                'url': url
            }), 400
            
    except Exception as e:
        print(f"❌ Erreur ajout URL: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Endpoint pour les statistiques"""
    try:
        # ✅ CORRECTION : NOUVELLE INSTANCE POUR AVOIR LES STATS FRAÎCHES
        qa_engine = get_fresh_qa_engine()
        stats = qa_engine.get_system_stats()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'OK', 'message': 'API RAG fonctionnelle'})

@app.route('/api/refresh', methods=['POST'])
def refresh_data():
    """Endpoint pour forcer le rafraîchissement des données"""
    try:
        # Cette méthode force le rechargement du VectorStore
        vector_store = get_fresh_vector_store()
        stats = vector_store.get_stats()
        return jsonify({
            'status': 'OK', 
            'message': 'Données rafraîchies',
            'stats': stats
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/files', methods=['GET'])
def get_processed_files():
    """Endpoint pour récupérer la liste des fichiers traités"""
    try:
        vector_store = get_fresh_vector_store()
        stats = vector_store.get_stats()
        
        # Récupérer les fichiers depuis le dossier processed
        processed_files = []
        if os.path.exists(config.config.PROCESSED_DIR):
            for filename in os.listdir(config.config.PROCESSED_DIR):
                if not filename.startswith('.'):
                    file_path = os.path.join(config.config.PROCESSED_DIR, filename)
                    file_size = os.path.getsize(file_path) / 1024 / 1024  # Taille en MB
                    processed_files.append({
                        'name': filename,
                        'size': f"{file_size:.2f} MB",
                        'processed': True
                    })
        
        return jsonify({
            'files': processed_files,
            'total_files': len(processed_files),
            'vector_store_stats': stats
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🎯 API RAG démarrée sur http://localhost:5000")
    print("📋 Endpoints disponibles:")
    print("   POST /api/ask - Poser une question")
    print("   POST /api/upload - Uploader un fichier") 
    print("   POST /api/process-url - Traiter une URL (réponse immédiate)")
    print("   POST /api/add-url - Ajouter une URL à la base")
    print("   GET  /api/stats - Obtenir les statistiques")
    print("   GET  /api/files - Obtenir la liste des fichiers traités")
    print("   POST /api/refresh - Rafraîchir les données")
    print("   GET  /api/health - Vérifier la santé de l'API")
    print("")
    print("⚡ IMPORTANT: Les instances sont recréées à chaque requête")
    print("   pour garantir des données fraîches !")
    app.run(debug=True, host='0.0.0.0', port=5000)