# JobMatch AI - Plateforme de matching CV / Offres d'emploi

JobMatch AI est une application web développée en Python qui permet de faire correspondre automatiquement des CV avec des offres d'emploi en utilisant des techniques de traitement du langage naturel (NLP).

## 🎯 Objectifs

- Automatiser le processus de tri des candidatures
- Réduire le temps de recherche d'emploi
- Appliquer des techniques simples de traitement de texte (NLP)
- Développer une application web complète avec base de données

## 🛠 Technologies utilisées

- **Python** (langage principal)
- **Flask** (framework web)
- **SQLite** (base de données légère)
- **scikit-learn** (TF-IDF + Similarité cosinus pour le matching)
- **HTML/CSS/Bootstrap** (interface utilisateur)

## 🧠 Principe technique

Le système utilise la méthode **TF-IDF** (Term Frequency - Inverse Document Frequency) pour transformer les textes en vecteurs numériques, puis calcule une **similarité cosinus** entre le CV et chaque offre d'emploi afin d'obtenir un score de compatibilité.

## 📦 Installation

### Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Étapes d'installation

1. **Cloner ou télécharger le projet**
   ```bash
   git clone <repository-url>
   cd JobMatchAI
   ```

2. **Créer un environnement virtuel (recommandé)**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialiser la base de données**
   ```bash
   python app.py
   ```
   La base de données SQLite sera créée automatiquement.

## 🚀 Lancement de l'application

```bash
python app.py
```

L'application sera accessible à l'adresse : **http://localhost:5000**

## 📋 Utilisation

### Pour les candidats

1. **Accéder à la page d'accueil**
2. **Coller votre CV** dans la zone de texte prévue à cet effet
3. **Facultatif :** Saisir votre email pour être contacté
4. **Cliquer sur "Analyser mon CV"**
5. **Consulter les résultats** classés par pourcentage de compatibilité

### Pour les administrateurs

1. **Accéder à l'interface d'administration** : http://localhost:5000/admin
2. **Ajouter des offres d'emploi** manuellement
3. **Initialiser les données exemples** pour tester rapidement
4. **Gérer les offres existantes** (suppression, modification)

## 🏗️ Structure du projet

```
JobMatchAI/
├── app.py                 # Application Flask principale
├── requirements.txt       # Dépendances Python
├── README.md             # Documentation
├── jobmatch.db           # Base de données SQLite (créée automatiquement)
├── templates/            # Fichiers HTML
│   ├── base.html        # Template de base
│   ├── index.html       # Page d'accueil
│   ├── results.html     # Page de résultats
│   ├── admin.html       # Interface d'administration
│   └── add_job.html     # Formulaire d'ajout d'offre
└── static/
    └── css/
        └── style.css    # Styles CSS personnalisés
```

## 📊 Fonctionnalités

### Matching intelligent
- **Analyse TF-IDF** pour extraire les mots-clés importants
- **Similarité cosinus** pour mesurer la pertinence
- **Classement automatique** des offres par score de compatibilité
- **Visualisation intuitive** avec barres de progression et couleurs

### Interface utilisateur
- **Design moderne et responsive** avec Bootstrap 5
- **Animations fluides** pour une meilleure expérience utilisateur
- **Système de notifications** pour les feedbacks utilisateurs
- **Interface d'administration** complète pour la gestion des offres

### Base de données
- **Modèle SQLAlchemy** pour les offres d'emploi
- **Historique des soumissions** de CV
- **Stockage des résultats** de matching
- **Données exemples** incluses pour les tests

## 🔧 Configuration

### Variables d'environnement (optionnelles)

```python
# Dans app.py
app.config['SECRET_KEY'] = 'votre_cle_secrete_ici'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jobmatch.db'
```

### Personnalisation du matching

Vous pouvez ajuster les paramètres du TF-IDF dans la fonction `calculate_similarity()` :

```python
vectorizer = TfidfVectorizer(
    stop_words='english',
    max_features=5000,      # Nombre maximum de features
    ngram_range=(1, 2)      # Unigrammes et bigrammes
)
```

## 🎨 Personnalisation

### Styles CSS
Les styles sont personnalisables dans `static/css/style.css` :
- Variables CSS pour les couleurs
- Animations et transitions
- Design responsive

### Templates HTML
Les templates utilisent le moteur Jinja2 :
- Héritage avec `base.html`
- Composants réutilisables
- Intégration Bootstrap 5

## 📈 Améliorations possibles

- **Support multilingue** (français, anglais, etc.)
- **Algorithmes de matching plus avancés** (Word2Vec, BERT)
- **Système de comptes utilisateurs**
- **Notifications par email**
- **API REST** pour l'intégration externe
- **Dashboard analytique** pour les recruteurs
- **Upload de fichiers CV** (PDF, DOCX)
- **Système de recommandation collaboratif**

## 🐛 Dépannage

### Problèmes courants

1. **Erreur d'importation**
   ```bash
   pip install -r requirements.txt
   ```

2. **Base de données vide**
   - Accédez à `/admin/init_sample_data` pour charger les exemples

3. **Port déjà utilisé**
   ```bash
   # Changer le port dans app.py
   app.run(debug=True, port=5001)
   ```

## 📝 Licence

Ce projet est développé à des fins éducatives et démonstratives.

## 👥 Contributeurs

Projet développé dans le cadre d'une démonstration des capacités de l'intelligence artificielle appliquée au recrutement.

---

**JobMatch AI** - L'IA qui connecte les bons talents aux bonnes opportunités ! 🚀
