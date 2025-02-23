import urllib.parse
import re

MUSIC_KEYWORDS = ["joue", "mets", "lance", "écoute", "écouter", "jouer", "musique", "deezer"]

def clean_music_query(question):
    """ Nettoie la requête musicale en supprimant les mots inutiles. """
    removal_words = MUSIC_KEYWORDS + ["peux-tu", "me", "le", "la", "les", "des", "du", "un", "une", "sur", "s'il te plaît"]
    pattern = r"\b(" + "|".join(re.escape(word) for word in removal_words) + r")\b"
    cleaned = re.sub(pattern, "", question, flags=re.IGNORECASE)
    return re.sub(r"\s+", " ", cleaned).strip()

def get_deezer_embed_url(query):
    """ Génère l'URL d'intégration Deezer avec le titre recherché. """
    cleaned_query = clean_music_query(query)
    search_url = f"https://www.deezer.com/search/{urllib.parse.quote(cleaned_query)}"
    return search_url, f"🎵 Lecture de '{cleaned_query}' sur Deezer."
