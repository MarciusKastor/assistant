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
                return f"🔍 Résultat pour '{query}':\nSnippet original:\n{snippet}\nRésumé:\n{summary}"
            else:
                return f"🔍 Aucun snippet trouvé pour '{query}'."
        else:
            return f"🔍 Aucun résultat trouvé pour '{query}'."
    except Exception as e:
        return f"Erreur lors de la recherche ou du résumé : {e}"
