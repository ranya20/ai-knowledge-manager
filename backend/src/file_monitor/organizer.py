# backend/src/file_monitor/organizer.py
import os
import shutil

class FileOrganizer:
    def __init__(self, config):
        self.config = config
        self._create_directories()
    
    def _create_directories(self):
        """Crée tous les dossiers nécessaires"""
        for directory in [self.config.INCOMING_DIR, self.config.PROCESSING_DIR, 
                         self.config.PROCESSED_DIR, self.config.FAILED_DIR]:
            os.makedirs(directory, exist_ok=True)
    
    def get_new_files(self):
        """Retourne la liste des nouveaux fichiers à traiter"""
        return [f for f in os.listdir(self.config.INCOMING_DIR) 
                if self._is_supported_format(f)]
    
    def _is_supported_format(self, filename):
        """Vérifie si le format est supporté"""
        ext = os.path.splitext(filename)[1].lower()
        all_formats = []
        for formats in self.config.SUPPORTED_FORMATS.values():
            all_formats.extend(formats)
        return ext in all_formats
    
    def move_to_processing(self, filename):
        """Déplace un fichier vers processing"""
        src = os.path.join(self.config.INCOMING_DIR, filename)
        dst = os.path.join(self.config.PROCESSING_DIR, filename)
        shutil.move(src, dst)
        return dst
    
    def move_to_processed(self, filename, success=True):
        """Déplace un fichier vers processed ou failed"""
        src = os.path.join(self.config.PROCESSING_DIR, filename)
        
        if success:
            dst = os.path.join(self.config.PROCESSED_DIR, filename)
        else:
            dst = os.path.join(self.config.FAILED_DIR, filename)
        
        shutil.move(src, dst)
        return dst