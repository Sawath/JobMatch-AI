import os
from app import app, db

print("🔍 Vérification SQLite")
print(f"📁 Répertoire: {os.getcwd()}")

# Chemin absolu de la base de données
db_path = os.path.join(os.getcwd(), 'jobmatch.db')
print(f"📂 Chemin DB: {db_path}")
print(f"📂 Fichier existe: {os.path.exists(db_path)}")

with app.app_context():
    # Forcer la création
    db.create_all()
    
    # Vérifier avec SQLAlchemy
    from app import JobOffer
    print(f"📊 Offres (SQLAlchemy): {JobOffer.query.count()}")
    
    # Vérifier le fichier
    if os.path.exists(db_path):
        print(f"📁 Taille fichier: {os.path.getsize(db_path)} bytes")
        
        import sqlite3
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"📋 Tables: {[t[0] for t in tables]}")
        
        if tables:
            cursor.execute("SELECT COUNT(*) FROM job_offer;")
            count = cursor.fetchone()[0]
            print(f"📊 Offres (SQLite): {count}")
            
            cursor.execute("SELECT title, company FROM job_offer LIMIT 3;")
            jobs = cursor.fetchall()
            print("📝 Exemples d'offres:")
            for job in jobs:
                print(f"  - {job[0]} chez {job[1]}")
        
        conn.close()
    else:
        print("❌ Fichier non trouvé")
