from app import app, db, User

with app.app_context():
    # Vérifier les utilisateurs
    users = User.query.all()
    print("👥 Utilisateurs dans la base:")
    for user in users:
        print(f"  - {user.username} (role: {user.role})")
    
    # Vérifier la route admin
    print(f"\n🔗 Route /admin existe: {'/admin' in [rule.rule for rule in app.url_map.iter_rules()]}")
    
    # Tester la génération d'URL
    with app.test_request_context():
        try:
            admin_url = app.url_for('admin')
            print(f"✅ URL admin générée: {admin_url}")
        except Exception as e:
            print(f"❌ Erreur génération URL admin: {e}")
