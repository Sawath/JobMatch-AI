from app import app, db, JobOffer
import os

print("🔍 Vérification de la persistance des données")
print(f"📁 Fichier DB: {os.path.exists('jobmatch.db')}")
print(f"📊 Taille DB: {os.path.getsize('jobmatch.db') if os.path.exists('jobmatch.db') else 0} bytes")

with app.app_context():
    jobs = JobOffer.query.all()
    print(f"📝 Nombre d'offres: {len(jobs)}")
    
    if jobs:
        print("\n📋 Liste des offres:")
        for job in jobs:
            print(f"  - {job.title} chez {job.company}")
            print(f"    📍 {job.location} | 💼 {job.contract_type}")
    else:
        print("❌ Aucune offre trouvée")
    
    print(f"\n💾 Configuration DB: {app.config['SQLALCHEMY_DATABASE_URI']}")
