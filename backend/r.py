import os
import shutil
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import config

def reset_system_complet():
    """Réinitialise complètement le système (vector_store + dossiers)"""
    print("🔄 RÉINITIALISATION COMPLÈTE DU SYSTÈME")
    print("=" * 50)
    
    confirmation = input("❌ ATTENTION: Cela supprimera TOUTES les données. Continuer? (oui/NON): ")
    if confirmation.lower() != 'oui':
        print("❌ Annulé.")
        return
    
    dossiers_a_vider = [
        config.config.PROCESSING_DIR,
        config.config.FAILED_DIR,
        config.config.VECTOR_STORE_PATH
    ]
    
    dossiers_a_conserver = [
        config.config.INCOMING_DIR,
        config.config.PROCESSED_DIR
    ]
    
    print("\n🗑️  SUPPRESSION:")
    for dossier in dossiers_a_vider:
        if os.path.exists(dossier):
            shutil.rmtree(dossier)
            os.makedirs(dossier)
            print(f"   ✅ {os.path.basename(dossier)}")
    
    print("\n📁 CONSERVATION:")
    for dossier in dossiers_a_conserver:
        if os.path.exists(dossier):
            file_count = len(os.listdir(dossier))
            print(f"   ✅ {os.path.basename(dossier)} ({file_count} fichiers)")
    
    print("\n🎯 SYSTÈME RÉINITIALISÉ!")
    print("   - Vector Store: VIDÉ")
    print("   - Processing/Failed: VIDÉS") 
    print("   - Incoming/Processed: CONSERVÉS")

if __name__ == "__main__":
    reset_system_complet()