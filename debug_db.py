import os
from app import app, db, JobOffer

print("🔍 Débogage de la base de données")
print(f"📁 Répertoire de travail: {os.getcwd()}")
print(f"🌐 Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")

with app.app_context():
    try:
        # Forcer la création des tables
        db.create_all()
        print("✅ Tables créées avec SQLAlchemy")
        
        # Vérifier avec SQLAlchemy
        job_count = JobOffer.query.count()
        print(f"📊 Nombre d'offres (SQLAlchemy): {job_count}")
        
        # Vérifier directement avec SQLite
        import sqlite3
        db_path = 'jobmatch.db'
        if os.path.exists(db_path):
            print(f"📁 Fichier DB existe: {os.path.getsize(db_path)} bytes")
            
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Lister les tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            print(f"📋 Tables SQLite: {[t[0] for t in tables]}")
            
            # Vérifier la table job_offer
            cursor.execute("SELECT COUNT(*) FROM job_offer;")
            count = cursor.fetchone()[0]
            print(f"📊 Nombre d'offres (SQLite): {count}")
            
            conn.close()
        else:
            print("❌ Fichier jobmatch.db n'existe pas")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
