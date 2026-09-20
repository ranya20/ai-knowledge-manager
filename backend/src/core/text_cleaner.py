import re
import string
from typing import List

class TextCleaner:
    """Classe pour nettoyer et prétraiter le texte extrait"""
    
    def __init__(self):
        # Patterns pour le nettoyage
        self.whitespace_pattern = re.compile(r'\s+')
        self.email_pattern = re.compile(r'\S+@\S+\.\S+')
        self.url_pattern = re.compile(r'http\S+')
        self.special_chars_pattern = re.compile(r'[^\w\s.,!?;:()\-]')
        
    def clean_text(self, text: str) -> str:
        """
        Nettoie le texte en appliquant plusieurs étapes de prétraitement
        """
        if not text:
            return ""
        
        # Convertir en string si nécessaire
        text = str(text)
        
        # Étape 1: Supprimer les URLs
        text = self.url_pattern.sub('', text)
        
        # Étape 2: Supprimer les emails
        text = self.email_pattern.sub('', text)
        
        # Étape 3: Supprimer les caractères spéciaux non désirés
        text = self.special_chars_pattern.sub('', text)
        
        # Étape 4: Normaliser les espaces blancs
        text = self.whitespace_pattern.sub(' ', text)
        
        # Étape 5: Supprimer les espaces en début et fin
        text = text.strip()
        
        # Étape 6: Remplacer les sauts de ligne multiples par un seul
        text = re.sub(r'\n+', '\n', text)
        
        # Étape 7: Capitaliser la première lettre si nécessaire
        if text and text[0].islower():
            text = text[0].upper() + text[1:]
        
        return text
    
    def clean_and_split_sentences(self, text: str) -> List[str]:
        """
        Nettoie le texte et le divise en phrases
        """
        cleaned_text = self.clean_text(text)
        
        # Diviser en phrases (règles simples)
        sentences = re.split(r'[.!?]+', cleaned_text)
        
        # Nettoyer chaque phrase
        clean_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 10:  # Ignorer les phrases trop courtes
                clean_sentences.append(sentence)
        
        return clean_sentences
    
    def remove_excessive_newlines(self, text: str, max_consecutive: int = 2) -> str:
        """
        Supprime les sauts de ligne excessifs
        """
        pattern = r'\n{' + str(max_consecutive + 1) + ',}'
        return re.sub(pattern, '\n' * max_consecutive, text)
    
    def normalize_whitespace(self, text: str) -> str:
        """
        Normalise tous les types d'espaces blancs
        """
        # Remplacer tous les espaces blancs par un espace simple
        text = re.sub(r'[ \t\r\f\v]+', ' ', text)
        return text.strip()
    
    def extract_clean_paragraphs(self, text: str) -> List[str]:
        """
        Extrait les paragraphes propres du texte
        """
        # Diviser par sauts de ligne
        paragraphs = text.split('\n')
        
        clean_paragraphs = []
        for paragraph in paragraphs:
            cleaned = self.clean_text(paragraph)
            if len(cleaned) > 20:  # Paragraphes significatifs seulement
                clean_paragraphs.append(cleaned)
        
        return clean_paragraphs

# Test du module
if __name__ == "__main__":
    cleaner = TextCleaner()
    
    # Test avec un texte sale
    dirty_text = """
    Voici un texte   avec   beaucoup   d'espaces.  
    Et aussi des sauts de ligne


    multiples !
    
    Contact: test@example.com
    Site: http://example.com/path
    Caractères #spéciaux @inutiles...
    """
    
    print("Texte original:")
    print(repr(dirty_text))
    print("\nTexte nettoyé:")
    cleaned = cleaner.clean_text(dirty_text)
    print(repr(cleaned))
    print("\nAffichage propre:")
    print(cleaned)