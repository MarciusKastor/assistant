import sqlite3
import json

def init_db():
    # Charger la configuration pour récupérer le chemin de la base de données
    with open("config/config.json", "r") as f:
        config = json.load(f)
    db_path = config["database"].get("path", "database.db")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Exemple de création d'une table "users"
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT,
      data TEXT
    )
    """)
    conn.commit()
    return conn
