import sqlite3

conn = sqlite3.connect('jobmatch.db')
cursor = conn.cursor()

# Lister toutes les tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("📋 Tables dans la base de données:")
for table in tables:
    print(f"  - {table[0]}")

# Vérifier la structure de chaque table
for table in tables:
    table_name = table[0]
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()
    print(f"\n🏗️ Structure de la table '{table_name}':")
    for col in columns:
        print(f"  - {col[1]} ({col[2]})")

# Compter les enregistrements
print(f"\n📊 Nombre d'enregistrements:")
for table in tables:
    table_name = table[0]
    cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
    count = cursor.fetchone()[0]
    print(f"  - {table_name}: {count}")

conn.close()
