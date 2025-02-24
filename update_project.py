#!/usr/bin/env python3
import os
import sys
import re

def backup_file(filepath):
    backup_path = filepath + ".bak"
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        with open(backup_path, "w", encoding="utf-8") as f_backup:
            f_backup.write(content)
        print(f"Sauvegarde effectuée dans {backup_path}.")
        return content
    except Exception as e:
        print(f"Erreur lors de la sauvegarde de {filepath} : {e}")
        sys.exit(1)

def update_dispatcher_file(filepath):
    content = backup_file(filepath)
    
    # Définition du bloc de code à insérer juste après la ligne où lower_question est définie
    new_block = '''\
    # --- Commande spéciale "arthena" pour activer la recherche Google avec résumé
    if lower_question.startswith("arthena "):
        query = lower_question[len("arthena "):].strip()
        from modules.commands.search import open_google_search_with_summary
        return open_google_search_with_summary(query)
'''
    # Recherche le pattern correspondant à "lower_question = question.lower().strip()"
    pattern = re.compile(r"(lower_question\s*=\s*question\.lower\(\)\.strip\(\))", re.IGNORECASE)
    if not pattern.search(content):
        print("La ligne de définition de lower_question n'a pas été trouvée.")
        sys.exit(1)
    
    # Insertion du bloc après la définition de lower_question
    new_content = pattern.sub(r"\1\n" + new_block, content)
    
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Le fichier {filepath} a été mis à jour avec la commande vocale 'arthena'.")
    except Exception as e:
        print(f"Erreur lors de l'écriture dans {filepath} : {e}")
        sys.exit(1)

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dispatcher_filepath = os.path.join(base_dir, "modules", "dispatcher.py")
    if not os.path.exists(dispatcher_filepath):
        print(f"Le fichier {dispatcher_filepath} n'existe pas.")
        sys.exit(1)
    update_dispatcher_file(dispatcher_filepath)

if __name__ == "__main__":
    main()
