from flask import Flask, url_for

app = Flask(__name__)

# Importer les routes depuis l'app principale
from app import app as main_app

with main_app.test_request_context():
    print("🔍 Test du bouton 'Gérer mes offres'")
    
    # Test 1: Vérifier si la route admin existe
    admin_routes = [rule for rule in main_app.url_map.iter_rules() if 'admin' in rule.rule]
    print(f"📋 Routes admin trouvées: {[rule.rule for rule in admin_routes]}")
    
    # Test 2: Générer l'URL
    try:
        admin_url = main_app.url_for('admin')
        print(f"✅ URL admin: {admin_url}")
    except Exception as e:
        print(f"❌ Erreur URL admin: {e}")
    
    # Test 3: Simuler un utilisateur recruteur
    with main_app.test_client() as client:
        # Simuler une session recruteur
        with client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['username'] = 'recruteur'
            sess['role'] = 'recruteur'
        
        # Tester l'accès à /admin
        response = client.get('/admin')
        print(f"🌐 Accès à /admin: Status {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Page admin accessible")
        elif response.status_code == 302:
            print("🔄 Redirection vers login")
        else:
            print(f"❌ Erreur: {response.status_code}")
