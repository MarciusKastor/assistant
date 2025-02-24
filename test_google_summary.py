#!/usr/bin/env python3
import os
import re
import sys

def create_search_with_summary():
    """
    Crée ou met à jour le module 'search_with_summary.py' dans modules/commands.
    Ce module implémente la recherche Google Custom Search et le résumé du snippet.
    """
    commands_dir = os.path.join("modules", "commands")
    if not os.path.exists(commands_dir):
        os.makedirs(commands_dir)
    target_path = os.path.join(commands_dir, "search_with_summary.py")
    
    code = '''\
import requests
from transformers import pipeline

API_KEY = "AIzaSyCSUqIYxuzAPcY4ZMJsUxfPcFvCKotNRMg"
CX = "212888795d83345dc"

def google_search(query):
    """Effectue une recherche sur Google Custom Search et renvoie le résultat JSON."""
    url = "https://www.googleapis.com/customsearch/v1"
    params = {"key": API_KEY, "cx": CX, "q": query}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def clean_text(text):
    """Nettoie le texte en supprimant les retours à la ligne et espaces superflus."""
    return " ".join(text.split())

_summarizer = None
def get_summarizer():
    global _summarizer
    if _summarizer is None:
        _summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    return _summarizer

def summarize_text(text, max_length=50, min_length=10):
    """
    Génère un résumé du texte donné.
    Les paramètres max_length et min_length permettent d'ajuster la longueur du résumé.
    """
    text = clean_text(text)
    summarizer = get_summarizer()
    summary_output = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
    return summary_output[0]['summary_text']

def open_google_search_with_summary(query):
    """
    Effectue une recherche Google via l'API Custom Search,
    récupère le snippet du premier résultat et renvoie
    une chaîne contenant le snippet original et son résumé.
    """
    try:
        results = google_search(query)
        if "items" in results and results["items"]:
            first_item = results["items"][0]
            snippet = first_item.get("snippet", "")
            if snippet:
                summary = summarize_text(snippet)
                return f"🔍 Résultat pour '{query}':\\nSnippet original:\\n{snippet}\\nRésumé:\\n{summary}"
            else:
                return f"🔍 Aucun snippet trouvé pour '{query}'."
        else:
            return f"🔍 Aucun résultat trouvé pour '{query}'."
    except Exception as e:
        return f"Erreur lors de la recherche ou du résumé : {e}"
'''
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(code)
    print("Module 'modules/commands/search_with_summary.py' créé/mis à jour.")

def update_dispatcher():
    """
    Ajoute un bloc dans modules/dispatcher.py pour intercepter les commandes
    commençant par "amélie " et appeler la fonction open_google_search_with_summary.
    Le bloc est inséré juste après la ligne définissant lower_question.
    """
    dispatcher_path = os.path.join("modules", "dispatcher.py")
    if not os.path.exists(dispatcher_path):
        print(f"Fichier {dispatcher_path} introuvable.")
        sys.exit(1)
    
    with open(dispatcher_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Si le bloc est déjà présent, on arrête.
    if 'if lower_question.startswith("amélie ")' in content:
        print("Le bloc 'Amélie' est déjà présent dans dispatcher.py.")
        return
    
    # On insère le bloc juste après la définition de lower_question.
    pattern = re.compile(r"(lower_question\s*=\s*question\.lower\(\)\.strip\(\))")
    new_block = r"""\1
    # --- Commande spéciale "Amélie" pour recherche avec résumé
    if lower_question.startswith("amélie "):
        query = lower_question[len("amélie "):].strip()
        from modules.commands.search_with_summary import open_google_search_with_summary
        return open_google_search_with_summary(query)"""
    new_content, count = pattern.subn(new_block, content, count=1)
    if count == 0:
        print("Impossible de trouver la définition de lower_question dans dispatcher.py.")
        sys.exit(1)
    
    # Sauvegarder une copie de secours
    backup_path = dispatcher_path + ".bak_amélie"
    with open(backup_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    with open(dispatcher_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Fichier 'modules/dispatcher.py' mis à jour avec la commande 'Amélie'.")

def main():
    create_search_with_summary()
    update_dispatcher()

if __name__ == "__main__":
    main()
