# backend/run.py
import sys
import os

# Forcer les imports absolus
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')

# Ajouter les deux chemins
sys.path.insert(0, current_dir)
sys.path.insert(0, src_dir)

print(f"📁 Répertoire backend: {current_dir}")
print(f"📁 Répertoire src: {src_dir}")

try:
    from src.main import KnowledgeManager
    print("✅ Import réussi!")
except ImportError as e:
    print(f"❌ Erreur import: {e}")
    print("📂 Liste des fichiers dans src/:")
    if os.path.exists(src_dir):
        for file in os.listdir(src_dir):
            print(f"   - {file}")
    sys.exit(1)

if __name__ == "__main__":
    print("🚀 Démarrage AI Knowledge Manager...")
    manager = KnowledgeManager()
    manager.run_continuous(interval=10)