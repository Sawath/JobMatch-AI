from app import app, db, User

with app.app_context():
    # Supprimer les utilisateurs existants
    User.query.delete()
    db.session.commit()
    
    # Créer un utilisateur recruteur
    recruteur = User(
        username='recruteur',
        email='recruteur@jobmatch.ai',
        role='recruteur'
    )
    recruteur.set_password('recruteur123')
    db.session.add(recruteur)
    
    # Créer un utilisateur candidat
    candidat = User(
        username='candidat',
        email='candidat@jobmatch.ai',
        role='candidat'
    )
    candidat.set_password('candidat123')
    db.session.add(candidat)
    
    db.session.commit()
    
    print("✅ Utilisateurs créés avec succès :")
    print("💼 Recruteur - username: recruteur, password: recruteur123")
    print("👤 Candidat - username: candidat, password: candidat123")
