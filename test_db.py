from app import app, db, JobOffer, CVSubmission, MatchResult

with app.app_context():
    # Créer les tables
    db.create_all()
    print("✅ Tables créées avec succès")
    
    # Vérifier les tables
    print(f"📊 Nombre d'offres: {JobOffer.query.count()}")
    print(f"📝 Nombre de CV: {CVSubmission.query.count()}")
    print(f"🎯 Nombre de matchs: {MatchResult.query.count()}")
    
    # Afficher les noms des tables
    import sqlite3
    conn = sqlite3.connect('jobmatch.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print(f"📋 Tables dans la base: {[table[0] for table in tables]}")
    conn.close()
