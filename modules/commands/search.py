import threading
import webbrowser
import urllib.parse
import re

COMMON_REMOVAL_WORDS = [
    "peux-tu", "peux", "tu", "me", "le", "la", "les", "des", "un", "une",
    "trouve", "montre-moi", "fais", "montre", "sur", "pour", "s'il te plaît"
]

GOOGLE_KEYWORDS = ["cherche", "recherche", "chercher"]
YOUTUBE_KEYWORDS = ["youtube", "cherche sur youtube", "recherche youtube", "chercher sur youtube"]

def clean_search_query(question, keywords):
    """ Nettoie la requête de recherche en supprimant les mots communs et les mots-clés spécifiques. """
    # Supprimer les mots communs
    pattern_common = r"\b(" + "|".join(re.escape(word) for word in COMMON_REMOVAL_WORDS) + r")\b"
    cleaned = re.sub(pattern_common, "", question, flags=re.IGNORECASE)

    # Supprimer les mots-clés spécifiques passés en paramètres
    pattern_keywords = r"\b(" + "|".join(re.escape(word) for word in keywords) + r")\b"
    cleaned = re.sub(pattern_keywords, "", cleaned, flags=re.IGNORECASE)

    # Nettoyer les espaces superflus
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    return cleaned if cleaned else "recherche"

def open_google_search(question):
    query = clean_search_query(question, GOOGLE_KEYWORDS)
    url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
    threading.Thread(target=webbrowser.open, args=(url,), daemon=True).start()
    return f"🔎 J'ai ouvert Google avec les résultats pour '{query}'."

def open_youtube_search(question):
    query = clean_search_query(question, YOUTUBE_KEYWORDS + GOOGLE_KEYWORDS)  # Ajout des mots de recherche communs
    url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
    threading.Thread(target=webbrowser.open, args=(url,), daemon=True).start()
    return f"📺 J'ai ouvert YouTube avec les résultats pour '{query}'."
