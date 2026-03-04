from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'votre_cle_secrete_ici'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.dirname(os.path.abspath(__file__)), 'jobmatch.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='candidat')  # 'candidat' or 'recruteur'
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_recruteur(self):
        return self.role == 'recruteur'
    
    def __repr__(self):
        return f'<User {self.username}>'

class JobOffer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    contract_type = db.Column(db.String(50), nullable=False)
    
    def __repr__(self):
        return f'<JobOffer {self.title}>'

class CVSubmission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(100), nullable=True)
    submission_date = db.Column(db.DateTime, server_default=db.func.now())
    
    def __repr__(self):
        return f'<CVSubmission {self.id}>'

class MatchResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cv_id = db.Column(db.Integer, db.ForeignKey('cv_submission.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job_offer.id'), nullable=False)
    similarity_score = db.Column(db.Float, nullable=False)
    match_date = db.Column(db.DateTime, server_default=db.func.now())
    
    cv = db.relationship('CVSubmission', backref='matches')
    job = db.relationship('JobOffer', backref='matches')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Veuillez vous connecter pour accéder à cette page', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def recruteur_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Veuillez vous connecter pour accéder à cette page', 'warning')
            return redirect(url_for('login'))
        
        user = User.query.get(session['user_id'])
        if not user or not user.is_recruteur():
            flash('Accès réservé aux recruteurs', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

def calculate_similarity(cv_text, job_offers):
    """Calcule la similarité entre le CV et les offres d'emploi"""
    if not job_offers:
        return []
    
    # Préparer les textes
    documents = [cv_text]
    job_texts = []
    
    for job in job_offers:
        combined_text = f"{job.title} {job.company} {job.description} {job.requirements}"
        job_texts.append(combined_text)
    
    documents.extend(job_texts)
    
    # Vectorisation TF-IDF
    vectorizer = TfidfVectorizer(
        stop_words='english',
        max_features=5000,
        ngram_range=(1, 2)
    )
    
    try:
        tfidf_matrix = vectorizer.fit_transform(documents)
        
        # Calculer la similarité cosinus entre le CV (index 0) et chaque offre
        cv_vector = tfidf_matrix[0:1]
        job_vectors = tfidf_matrix[1:]
        
        similarities = cosine_similarity(cv_vector, job_vectors)[0]
        
        # Associer les scores avec les offres
        results = []
        for i, job in enumerate(job_offers):
            results.append({
                'job': job,
                'score': similarities[i],
                'percentage': round(similarities[i] * 100, 2)
            })
        
        # Trier par score décroissant
        results.sort(key=lambda x: x['score'], reverse=True)
        
        return results
        
    except Exception as e:
        print(f"Erreur lors du calcul de similarité: {e}")
        return []

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        if not username or not password:
            flash('Veuillez remplir tous les champs', 'danger')
            return render_template('login.html')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            flash(f'Bienvenue {user.username} !', 'success')
            return redirect(url_for('index'))
        else:
            flash('Identifiants incorrects', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()
        role = request.form.get('role', 'candidat')
        
        if not all([username, email, password, confirm_password]):
            flash('Veuillez remplir tous les champs', 'danger')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Les mots de passe ne correspondent pas', 'danger')
            return render_template('register.html')
        
        if User.query.filter_by(username=username).first():
            flash('Ce nom d\'utilisateur existe déjà', 'danger')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Cet email est déjà utilisé', 'danger')
            return render_template('register.html')
        
        user = User(username=username, email=email, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Compte créé avec succès ! Vous pouvez maintenant vous connecter', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Vous avez été déconnecté', 'info')
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/match', methods=['POST'])
@login_required
def match_cv():
    cv_content = request.form.get('cv_content', '').strip()
    email = request.form.get('email', '').strip()
    
    if not cv_content:
        flash('Veuillez saisir le contenu de votre CV', 'error')
        return redirect(url_for('index'))
    
    # Sauvegarder le CV
    cv_submission = CVSubmission(content=cv_content, email=email)
    db.session.add(cv_submission)
    db.session.commit()
    
    # Récupérer toutes les offres d'emploi
    job_offers = JobOffer.query.all()
    
    if not job_offers:
        flash('Aucune offre d\'emploi disponible dans la base de données', 'info')
        return redirect(url_for('index'))
    
    # Calculer les similarités
    matches = calculate_similarity(cv_content, job_offers)
    
    # Sauvegarder les résultats
    for match in matches:
        match_result = MatchResult(
            cv_id=cv_submission.id,
            job_id=match['job'].id,
            similarity_score=match['score']
        )
        db.session.add(match_result)
    
    db.session.commit()
    
    return render_template('results.html', matches=matches, cv_content=cv_content)

@app.route('/jobs')
def jobs_list():
    job_offers = JobOffer.query.all()
    
    # Filtrage
    search = request.args.get('search', '').lower()
    location = request.args.get('location', '')
    contract_type = request.args.get('contract_type', '')
    
    filtered_jobs = job_offers
    
    if search:
        filtered_jobs = [job for job in filtered_jobs 
                        if search in job.title.lower() or search in job.company.lower()]
    
    if location:
        filtered_jobs = [job for job in filtered_jobs if job.location == location]
    
    if contract_type:
        filtered_jobs = [job for job in filtered_jobs if job.contract_type == contract_type]
    
    return render_template('jobs_list.html', job_offers=job_offers, filtered_jobs=filtered_jobs)

@app.route('/job/<int:job_id>')
def job_detail(job_id):
    job = JobOffer.query.get_or_404(job_id)
    return render_template('job_detail.html', job=job)

@app.route('/admin')
@recruteur_required
def admin():
    job_offers = JobOffer.query.all()
    return render_template('admin.html', job_offers=job_offers)

@app.route('/admin/add_job', methods=['GET', 'POST'])
@recruteur_required
def add_job():
    if request.method == 'POST':
        job = JobOffer(
            title=request.form['title'],
            company=request.form['company'],
            description=request.form['description'],
            requirements=request.form['requirements'],
            location=request.form['location'],
            contract_type=request.form['contract_type']
        )
        db.session.add(job)
        db.session.commit()
        flash('Offre d\'emploi ajoutée avec succès', 'success')
        return redirect(url_for('admin'))
    
    return render_template('add_job.html')

@app.route('/admin/delete_job/<int:job_id>')
@recruteur_required
def delete_job(job_id):
    job = JobOffer.query.get_or_404(job_id)
    
    # Supprimer d'abord les match_results liés à cette offre
    MatchResult.query.filter_by(job_id=job_id).delete()
    
    # Puis supprimer l'offre
    db.session.delete(job)
    db.session.commit()
    flash('Offre d\'emploi supprimée avec succès', 'success')
    return redirect(url_for('admin'))

# Supprimer la route d'initialisation des données exemples
# @app.route('/admin/init_sample_data')
# @recruteur_required
# def init_sample_data():
#     """Initialiser la base de données avec des exemples d'offres d'emploi"""
#     pass

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Vérifier s'il y a des utilisateurs, sinon créer des comptes par défaut
        if User.query.count() == 0:
            # Créer un utilisateur recruteur par défaut
            recruteur = User(
                username='recruteur',
                email='recruteur@jobmatch.ai',
                role='recruteur'
            )
            recruteur.set_password('recruteur123')
            db.session.add(recruteur)
            
            # Créer un utilisateur candidat par défaut
            candidat = User(
                username='candidat',
                email='candidat@jobmatch.ai',
                role='candidat'
            )
            candidat.set_password('candidat123')
            db.session.add(candidat)
            
            # Créer un utilisateur yann par défaut
            yann = User(
                username='yann',
                email='yann@jobmatch.ai',
                role='candidat'
            )
            yann.set_password('yann123')
            db.session.add(yann)
            
            db.session.commit()
            print("Comptes par défaut créés:")
            print("- Recruteur: username='recruteur', password='recruteur123'")
            print("- Candidat: username='candidat', password='candidat123'")
            print("- Yann: username='yann', password='yann123'")
        else:
            print(f"Base de données contient déjà {User.query.count()} utilisateur(s)")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
