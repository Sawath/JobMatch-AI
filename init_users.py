from app import app, db, User

with app.app_context():
    # Supprimer les utilisateurs existants
    User.query.delete()
    db.session.commit()
    
    # Créer un utilisateur admin
    admin = User(
        username='admin',
        email='admin@jobmatch.ai',
        role='admin'
    )
    admin.set_password('admin123')
    db.session.add(admin)
    
    # Créer un utilisateur candidat
    candidat = User(
        username='candidat',
        email='candidat@jobmatch.ai',
        role='user'
    )
    candidat.set_password('candidat123')
    db.session.add(candidat)
    
    db.session.commit()
    
    print("✅ Utilisateurs créés avec succès :")
    print("🔑 Admin - username: admin, password: admin123")
    print("👤 Candidat - username: candidat, password: candidat123")
