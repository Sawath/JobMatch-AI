from app import app, db, JobOffer

with app.app_context():
    # Supprimer et recréer les tables
    db.drop_all()
    db.create_all()
    print("✅ Base de données réinitialisée")
    
    # Ajouter les données exemples
    sample_jobs = [
        {
            'title': 'Développeur Python Senior',
            'company': 'TechCorp',
            'description': 'Nous recherchons un développeur Python expérimenté pour rejoindre notre équipe de développement backend. Vous travaillerez sur des projets innovants dans le domaine de l\'intelligence artificielle et du machine learning.',
            'requirements': 'Python, Django, Flask, PostgreSQL, Docker, Git, 5+ ans d\'expérience, Machine Learning, REST API',
            'location': 'Paris',
            'contract_type': 'CDI'
        },
        {
            'title': 'Data Scientist',
            'company': 'DataTech Solutions',
            'description': 'Rejoignez notre équipe de data scientists pour développer des modèles prédictifs et analyser des données complexes. Vous travaillerez sur des projets variés dans différents secteurs.',
            'requirements': 'Python, R, SQL, Machine Learning, Deep Learning, TensorFlow, PyTorch, Statistiques, Visualisation de données',
            'location': 'Lyon',
            'contract_type': 'CDI'
        },
        {
            'title': 'Développeur Full Stack JavaScript',
            'company': 'WebDev Agency',
            'description': 'Nous recherchons un développeur full stack passionné par les technologies web modernes. Vous participerez au développement complet d\'applications web pour nos clients.',
            'requirements': 'JavaScript, React, Node.js, MongoDB, Express.js, HTML5, CSS3, Git, Agile',
            'location': 'Remote',
            'contract_type': 'CDI'
        },
        {
            'title': 'Ingénieur DevOps',
            'company': 'CloudTech',
            'description': 'Nous cherchons un ingénieur DevOps pour améliorer notre infrastructure cloud et automatiser nos processus de déploiement. Vous travaillerez avec les dernières technologies DevOps.',
            'requirements': 'AWS, Azure, Docker, Kubernetes, CI/CD, Linux, Python, Ansible, Terraform, Monitoring',
            'location': 'Marseille',
            'contract_type': 'CDI'
        },
        {
            'title': 'Développeur Mobile iOS/Android',
            'company': 'AppStudio',
            'description': 'Rejoignez notre équipe de développement mobile pour créer des applications innovantes pour iOS et Android. Vous travaillerez sur des projets variés pour des clients prestigieux.',
            'requirements': 'Swift, Kotlin, React Native, Flutter, iOS, Android, REST API, Git, Agile, Xcode, Android Studio',
            'location': 'Bordeaux',
            'contract_type': 'CDD'
        }
    ]
    
    for job_data in sample_jobs:
        job = JobOffer(**job_data)
        db.session.add(job)
    
    db.session.commit()
    print(f"✅ {len(sample_jobs)} offres d'emploi ajoutées")
    print(f"📊 Total d'offres: {JobOffer.query.count()}")
