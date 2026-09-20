# backend/src/models/nlp_processor.py
import numpy as np
import re
import requests
from typing import List, Dict, Tuple
from collections import Counter
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import json
import os

# Télécharger les données NLTK si nécessaires
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

class NLPProcessor:
    def __init__(self, use_advanced_models: bool = True):
        self.use_advanced_models = use_advanced_models
        self.models_loaded = False
        self._load_models()
        print("✅ NLP Processor avancé initialisé")
    
    def _load_models(self):
        """Charge les modèles les plus performants avec fallback intelligent"""
        try:
            # === METHODE 1: Essaye d'abord les transformers modernes ===
            if self.use_advanced_models:
                self._load_advanced_models()
            
            # === METHODE 2: Fallback sur sentence-transformers ===
            if not self.models_loaded:
                self._load_sentence_transformers()
            
            # === METHODE 3: Fallback sur méthodes classiques ===
            if not self.models_loaded:
                self._load_classical_methods()
                
        except Exception as e:
            print(f"⚠️  Erreur chargement modèles: {e}")
            self._setup_ultimate_fallback()
    
    def _load_advanced_models(self):
        """Charge les modèles transformers les plus performants"""
        try:
            print("🚀 Chargement des modèles avancés...")
            
            # === RÉSUMÉ - Meilleur modèle français ===
            from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
            
            # Modèle de résumé spécialisé français
            self.summarizer = pipeline(
                "summarization",
                model="moussaKam/barthez-orangesum-abstract",
                tokenizer="moussaKam/barthez-orangesum-abstract"
            )
            
            # === EMBEDDINGS - Modèle multilingue performant ===
            from sentence_transformers import SentenceTransformer
            self.embedder = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
            
            # === EXTRACTION MOTS-CLÉS - Modèle spécialisé ===
            try:
                from keybert import KeyBERT
                self.keyword_model = KeyBERT(model='paraphrase-MiniLM-L3-v2')
            except:
                self.keyword_model = None
            
            # === CATÉGORISATION - Modèle zero-shot ===
            try:
                from transformers import pipeline as zpipeline
                self.classifier = zpipeline(
                    "zero-shot-classification",
                    model="BaptisteDoyen/camembert-base-xnli"
                )
            except:
                self.classifier = None
            
            self.models_loaded = True
            print("🎯 Modèles avancés chargés avec succès!")
            
        except Exception as e:
            print(f"❌ Échec modèles avancés: {e}")
            self.models_loaded = False
    
    def _load_sentence_transformers(self):
        """Charge sentence-transformers (bon compromis performance/mémoire)"""
        try:
            print("🔧 Chargement sentence-transformers...")
            from sentence_transformers import SentenceTransformer
            
            self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
            self.summarizer = None
            self.keyword_model = None
            self.classifier = None
            
            self.models_loaded = True
            print("✅ Sentence-transformers chargés")
            
        except Exception as e:
            print(f"❌ Échec sentence-transformers: {e}")
            self.models_loaded = False
    
    def _load_classical_methods(self):
        """Charge les méthodes classiques (fallback léger)"""
        try:
            print("📚 Chargement méthodes classiques...")
            
            # Pas de modèles lourds, on utilise des méthodes algorithmiques
            self.embedder = None
            self.summarizer = None
            self.keyword_model = None
            self.classifier = None
            
            self.models_loaded = True
            print("✅ Méthodes classiques chargées")
            
        except Exception as e:
            print(f"❌ Échec méthodes classiques: {e}")
            self.models_loaded = False
    
    def _setup_ultimate_fallback(self):
        """Fallback ultime - méthodes basiques"""
        print("🆘 Activation mode basique")
        self.models_loaded = True  # On considère que les méthodes basiques sont toujours disponibles
    
    def analyze_document(self, text: str, title: str = "", doc_type: str = "") -> Dict:
        """Analyse complète et intelligente d'un document"""
        if not text.strip():
            return self._empty_response()
        
        print(f"🔍 Analyse NLP avancée...")
        
        try:
            # Pré-traitement intelligent du texte
            clean_text = self._advanced_text_preprocessing(text, doc_type)
            
            # === RÉSUMÉ AUTOMATIQUE ===
            summary = self._advanced_summarization(clean_text, doc_type)
            
            # === EXTRACTION MOTS-CLÉS INTELLIGENTE ===
            keywords = self._advanced_keyword_extraction(clean_text, title)
            
            # === CATÉGORISATION AUTOMATIQUE ===
            category, confidence = self._advanced_categorization(clean_text, title)
            
            # === EMBEDDING POUR RECHERCHE ===
            embedding = self._get_advanced_embedding(clean_text)
            
            # === ANALYSE THÉMATIQUE ===
            themes = self._extract_themes(clean_text)
            
            # === SCORE DE QUALITÉ ===
            quality_score = self._calculate_quality_score(clean_text, summary, keywords)
            
            return {
                "summary": summary,
                "keywords": keywords,
                "category": category,
                "category_confidence": confidence,
                "themes": themes,
                "embedding": embedding,
                "quality_score": quality_score,
                "analysis_method": self._get_analysis_method(),
                "word_count": len(clean_text.split()),
                "analysis_success": True
            }
            
        except Exception as e:
            print(f"❌ Erreur analyse avancée: {e}")
            return self._fallback_analysis(text, title)
    
    def _advanced_summarization(self, text: str, doc_type: str) -> str:
        """Résumé automatique avec la meilleure méthode disponible"""
        # Ajuster la longueur selon le type de document
        length_config = {
            "academic": {"max_length": 200, "min_length": 80},
            "technical": {"max_length": 150, "min_length": 60},
            "general": {"max_length": 120, "min_length": 40}
        }
        
        config = length_config.get(doc_type, length_config["general"])
        
        # Méthode 1: Transformers avancés
        if self.summarizer:
            try:
                return self._transformer_summary(text, config)
            except:
                pass
        
        # Méthode 2: Algorithme extractif avancé
        return self._advanced_extractive_summary(text, config)
    
    def _transformer_summary(self, text: str, config: Dict) -> str:
        """Résumé avec transformers"""
        # Adapter la longueur selon la taille du texte
        input_length = len(text.split())
        max_len = min(config["max_length"], input_length // 2)
        min_len = min(config["min_length"], max_len // 2)
        
        summary = self.summarizer(
            text,
            max_length=max_len,
            min_length=min_len,
            do_sample=False,
            clean_up_tokenization_spaces=True
        )[0]['summary_text']
        
        return summary.strip()
    
    def _advanced_extractive_summary(self, text: str, config: Dict) -> str:
        """Résumé extractif intelligent"""
        try:
            from sumy.parsers.plaintext import PlaintextParser
            from sumy.nlp.tokenizers import Tokenizer
            from sumy.summarizers.lsa import LsaSummarizer
            from sumy.summarizers.text_rank import TextRankSummarizer
            
            # Essayer TextRank d'abord (meilleur pour la cohérence)
            parser = PlaintextParser.from_string(text, Tokenizer("french"))
            summarizer = TextRankSummarizer()
            
            # Nombre de phrases selon la longueur du texte
            sentences = text.split('.')
            summary_length = max(2, min(5, len(sentences) // 4))
            
            summary_sentences = summarizer(parser.document, summary_length)
            summary = ". ".join(str(sentence) for sentence in summary_sentences)
            
            if summary.strip():
                return summary + "."
                
        except Exception as e:
            print(f"⚠️  Sumy non disponible: {e}")
        
        # Fallback: Méthode TF-IDF personnalisée
        return self._tfidf_summary(text, config)
    
    def _tfidf_summary(self, text: str, config: Dict) -> str:
        """Résumé par TF-IDF personnalisé"""
        sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
        
        if len(sentences) <= 3:
            return text[:config["max_length"]] + "..."
        
        # Calcul TF-IDF simple
        vectorizer = TfidfVectorizer(stop_words=self._get_stopwords())
        try:
            tfidf_matrix = vectorizer.fit_transform(sentences)
            sentence_scores = tfidf_matrix.sum(axis=1).A1
            
            # Prendre les meilleures phrases
            top_indices = sentence_scores.argsort()[-3:][::-1]
            top_sentences = [sentences[i] for i in sorted(top_indices)]
            
            return ". ".join(top_sentences) + "."
        except:
            # Fallback basique
            return ". ".join(sentences[:3]) + "..."
    
    def _advanced_keyword_extraction(self, text: str, title: str = "") -> List[str]:
        """Extraction de mots-clés avec multiples méthodes"""
        all_keywords = []
        
        # Méthode 1: KeyBERT (si disponible)
        if self.keyword_model:
            try:
                keywords = self.keyword_model.extract_keywords(
                    text, 
                    keyphrase_ngram_range=(1, 2), 
                    stop_words='french',
                    top_n=8
                )
                all_keywords.extend([kw[0] for kw in keywords])
            except:
                pass
        
        # Méthode 2: RAKE (Rapid Automatic Keyword Extraction)
        rake_keywords = self._rake_keywords(text)
        all_keywords.extend(rake_keywords)
        
        # Méthode 3: TF-IDF classique
        tfidf_keywords = self._tfidf_keywords(text)
        all_keywords.extend(tfidf_keywords)
        
        # Méthode 4: Mots du titre (importants)
        if title:
            title_keywords = self._extract_title_keywords(title)
            all_keywords.extend(title_keywords)
        
        # Nettoyer et dédupliquer
        clean_keywords = list(set([
            kw.lower().strip() for kw in all_keywords 
            if len(kw) > 2 and kw not in self._get_stopwords()
        ]))
        
        # Classer par pertinence
        keyword_scores = {}
        for kw in clean_keywords:
            score = text.lower().count(kw.lower())
            if kw in title.lower():
                score *= 2  # Bonus pour les mots du titre
            keyword_scores[kw] = score
        
        # Retourner les meilleurs mots-clés
        return sorted(keyword_scores.keys(), key=lambda x: keyword_scores[x], reverse=True)[:10]
    
    def _rake_keywords(self, text: str) -> List[str]:
        """Extraction RAKE simplifiée"""
        # Implémentation simplifiée de RAKE
        words = re.findall(r'\b[a-zA-ZÀ-ÿ]{3,}\b', text.lower())
        stopwords = self._get_stopwords()
        
        # Filtrer les stopwords
        content_words = [w for w in words if w not in stopwords]
        
        # Compter les fréquences
        word_freq = Counter(content_words)
        return [word for word, count in word_freq.most_common(15)]
    
    def _tfidf_keywords(self, text: str) -> List[str]:
        """Mots-clés par TF-IDF"""
        try:
            vectorizer = TfidfVectorizer(
                stop_words=self._get_stopwords(),
                ngram_range=(1, 2),
                max_features=20
            )
            tfidf_matrix = vectorizer.fit_transform([text])
            feature_names = vectorizer.get_feature_names_out()
            
            # Obtenir les scores
            scores = tfidf_matrix.toarray().flatten()
            sorted_indices = scores.argsort()[::-1]
            
            return [feature_names[i] for i in sorted_indices[:10]]
        except:
            return []
    
    def _extract_title_keywords(self, title: str) -> List[str]:
        """Extrait les mots-clés du titre"""
        words = re.findall(r'\b[a-zA-ZÀ-ÿ]{3,}\b', title.lower())
        stopwords = self._get_stopwords()
        return [w for w in words if w not in stopwords]
    
    def _advanced_categorization(self, text: str, title: str = "") -> Tuple[str, float]:
        """Catégorisation automatique avancée"""
        full_text = (title + " " + text).lower()
        
        # Catégories avec mots-clés pondérés
        categories = {
            'technologie': [
                'python', 'programmation', 'code', 'algorithm', 'données', 'intelligence',
                'artificielle', 'machine learning', 'ai', 'développement', 'software'
            ],
            'éducation': [
                'étude', 'recherche', 'université', 'thèse', 'mémoire', 'apprentissage',
                'enseignement', 'cours', 'étudiant', 'professeur', 'pédagogie'
            ],
            'histoire': [
                'historique', 'siècle', 'révolution', 'époque', 'passé', 'ancien',
                'moyen âge', 'antique', 'historien', 'archéologie', 'chronique'
            ],
            'science': [
                'scientifique', 'recherche', 'expérience', 'découverte', 'laboratoire',
                'physique', 'chimie', 'biologie', 'médecine', 'recherche'
            ],
            'philosophie': [
                'pensée', 'réflexion', 'concept', 'idée', 'philosophique', 'morale',
                'éthique', 'existence', 'conscience', 'métaphysique'
            ],
            'droit': [
                'loi', 'juridique', 'droit', 'justice', 'tribunal', 'avocat',
                'procès', 'légal', 'constitution', 'jurisprudence'
            ],
            'économie': [
                'économie', 'marché', 'finance', 'entreprise', 'commerce', 'argent',
                'investissement', 'capital', 'bourse', 'croissance'
            ],
            'santé': [
                'médecine', 'santé', 'maladie', 'traitement', 'médical', 'hôpital',
                'patient', 'thérapie', 'diagnostic', 'prévention'
            ]
        }
        
        best_category = "général"
        best_score = 0
        
        for category, keywords in categories.items():
            score = 0
            for keyword in keywords:
                if keyword in full_text:
                    # Pondération selon la position
                    if keyword in title.lower():
                        score += 3  # Forte pondération pour le titre
                    else:
                        score += 1
            
            if score > best_score:
                best_score = score
                best_category = category
        
        # Calcul de confiance
        confidence = min(1.0, best_score / 10.0)
        
        return best_category, confidence
    
    def _extract_themes(self, text: str) -> List[str]:
        """Extraction de thèmes principaux"""
        keywords = self._advanced_keyword_extraction(text)
        
        # Regrouper les mots-clés similaires
        themes = []
        for keyword in keywords[:5]:
            # Simplification: chaque mot-clé important est un thème
            themes.append(keyword.capitalize())
        
        return themes
    
    def _get_advanced_embedding(self, text: str) -> List[float]:
        """Génère un embedding avancé"""
        if self.embedder:
            return self.embedder.encode([text])[0].tolist()
        else:
            # Fallback: embedding TF-IDF basique
            return self._tfidf_embedding(text)
    
    def _tfidf_embedding(self, text: str) -> List[float]:
        """Embedding TF-IDF de fallback"""
        try:
            vectorizer = TfidfVectorizer(
                stop_words=self._get_stopwords(),
                max_features=100
            )
            embedding = vectorizer.fit_transform([text]).toarray()[0]
            return embedding.tolist()
        except:
            return [0.0] * 100
    
    def _calculate_quality_score(self, text: str, summary: str, keywords: List[str]) -> float:
        """Calcule un score de qualité de l'analyse"""
        score = 0.0
        
        # Score basé sur la longueur du résumé
        if summary and len(summary) > 20:
            score += 0.3
        
        # Score basé sur les mots-clés
        if keywords and len(keywords) >= 3:
            score += 0.3
        
        # Score basé sur la longueur du texte
        if len(text.split()) > 50:
            score += 0.2
        
        # Score basé sur la diversité lexicale
        words = text.split()
        unique_words = set(words)
        if len(words) > 0:
            lexical_diversity = len(unique_words) / len(words)
            score += lexical_diversity * 0.2
        
        return min(1.0, score)
    
    def _advanced_text_preprocessing(self, text: str, doc_type: str) -> str:
        """Prétraitement intelligent du texte"""
        # Supprimer les marqueurs techniques
        text = re.sub(r'--- Page \d+ ---', '', text)
        text = re.sub(r'\n+', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        
        # Nettoyage spécifique selon le type
        if doc_type == "pdf_scanned":
            # Corrections OCR communes
            corrections = {
                r'\b1\b': 'l', r'\b0\b': 'o', r'\b5\b': 's',
                r'\b\[\b': 'l', r'\b\|\b': 'l', r'\b_\b': ''
            }
            for wrong, correct in corrections.items():
                text = re.sub(wrong, correct, text)
        
        return text.strip()
    
    def _get_stopwords(self):
        """Retourne les stopwords français"""
        try:
            from nltk.corpus import stopwords
            return set(stopwords.words('french'))
        except:
            return {
                'le', 'la', 'les', 'de', 'du', 'des', 'un', 'une', 'et', 'ou',
                'dans', 'pour', 'avec', 'sur', 'par', 'est', 'son', 'ses', 'ces'
            }
    
    def _get_analysis_method(self) -> str:
        """Retourne la méthode d'analyse utilisée"""
        if self.summarizer and self.keyword_model:
            return "transformers_avancés"
        elif self.embedder:
            return "sentence_transformers"
        else:
            return "méthodes_classiques"
    
    def _fallback_analysis(self, text: str, title: str = "") -> Dict:
        """Analyse de fallback"""
        clean_text = self._advanced_text_preprocessing(text, "")
        
        return {
            "summary": self._advanced_extractive_summary(clean_text, {"max_length": 100, "min_length": 30}),
            "keywords": self._advanced_keyword_extraction(clean_text, title),
            "category": "général",
            "category_confidence": 0.5,
            "themes": [],
            "embedding": self._get_advanced_embedding(clean_text),
            "quality_score": 0.5,
            "analysis_method": "fallback",
            "word_count": len(clean_text.split()),
            "analysis_success": False
        }
    
    def _empty_response(self) -> Dict:
        """Réponse pour texte vide"""
        return {
            "summary": "",
            "keywords": [],
            "category": "inconnu",
            "category_confidence": 0.0,
            "themes": [],
            "embedding": [],
            "quality_score": 0.0,
            "analysis_method": "aucun",
            "word_count": 0,
            "analysis_success": False
        }

# Test complet
if __name__ == "__main__":
    print("🧪 Test NLP Processor Complet...")
    
    # Test avec différents types de documents
    test_cases = [
        {
            "title": "Olympe de Gouges et les droits des femmes",
            "text": """
            Olympe de Gouges est une femme de lettres qui s'inscrit dans le mouvement des lumières 
            par ses œuvres progressistes qui œuvrent pour l'égalité. Le texte étudié représente 
            le postambule de Déclaration des droits de la femme et de la citoyenne, rédigée en 1791. 
            Ce postambule est un texte rhétorique qui est un appel à la lutte pour l'égalité des sexes.
            Elle constate le mépris des femmes malgré la Révolution et le rôle qu'elles ont joué dans 
            l'Histoire et propose donc des solutions à ce désintérêt.
            """,
            "type": "histoire"
        },
        {
            "title": "Introduction au Machine Learning",
            "text": """
            Le machine learning est une branche de l'intelligence artificielle qui permet aux ordinateurs 
            d'apprendre à partir de données sans être explicitement programmés. Les algorithmes de 
            machine learning sont utilisés dans de nombreux domaines comme la reconnaissance d'images, 
            le traitement du langage naturel, et la recommandation de contenu. Les réseaux de neurones 
            profonds ont révolutionné ce domaine ces dernières années.
            """,
            "type": "technologie"
        }
    ]
    
    nlp = NLPProcessor(use_advanced_models=True)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*60}")
        print(f"📄 TEST {i}: {test_case['title']}")
        print(f"{'='*60}")
        
        result = nlp.analyze_document(
            test_case['text'], 
            test_case['title'], 
            test_case['type']
        )
        
        print(f"✅ Méthode: {result['analysis_method']}")
        print(f"📝 Résumé: {result['summary']}")
        print(f"🔑 Mots-clés: {', '.join(result['keywords'][:8])}")
        print(f"🏷️ Catégorie: {result['category']} (confiance: {result['category_confidence']:.2f})")
        print(f"🎯 Thèmes: {', '.join(result['themes'])}")
        print(f"📊 Score qualité: {result['quality_score']:.2f}")
        print(f"📏 Mots analysés: {result['word_count']}")
    
    print(f"\n🎯 Test NLP Processor terminé avec succès!")