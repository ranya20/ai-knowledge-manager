# backend/check_structure.py
import os

def check_structure():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"📁 Base directory: {base_dir}")
    
    required_files = [
        'config.py',
        'run.py',
        'src/main.py',
        'src/core/pdf_processor.py',
        'src/core/ocr_processor.py', 
        'src/core/document_processor.py',
        'src/file_monitor/organizer.py'
    ]
    
    print("\n🔍 Vérification des fichiers:")
    all_exist = True
    for file in required_files:
        path = os.path.join(base_dir, file)
        exists = os.path.exists(path)
        status = "✅" if exists else "❌"
        print(f"   {status} {file}")
        if not exists:
            all_exist = False
    
    print(f"\n📂 Contenu de src/:")
    src_dir = os.path.join(base_dir, 'src')
    if os.path.exists(src_dir):
        for root, dirs, files in os.walk(src_dir):
            level = root.replace(src_dir, '').count(os.sep)
            indent = ' ' * 2 * level
            print(f'{indent}{os.path.basename(root)}/')
            sub_indent = ' ' * 2 * (level + 1)
            for file in files:
                if file.endswith('.py'):
                    print(f'{sub_indent}{file}')
    else:
        print("❌ Dossier src/ n'existe pas!")
    
    return all_exist

if __name__ == "__main__":
    if check_structure():
        print("\n🎯 Structure OK - Les imports devraient fonctionner")
    else:
        print("\n⚠️  Structure incomplète - Fichiers manquants")