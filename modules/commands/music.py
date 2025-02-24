# -*- coding: utf-8 -*-
"""
Module : music.py
Gère les commandes "Music" pour jouer de la musique via YouTube Music
en utilisant la bibliothèque ytmusicapi (OAuth ou cookies).
"""

import os
from ytmusicapi import YTMusic

# Par défaut, on suppose que tu utilises "oauth.json" (créé par 'ytmusicapi oauth').
# Si tu préfères la méthode cookies, remplace ici par "headers_auth.json".
OAUTH_FILE = os.path.join(os.path.dirname(__file__), '..', '..', 'oauth.json')

ytmusic = None

def init_ytmusic():
    """Initialise l'API YouTube Music (OAuth ou cookies)."""
    global ytmusic
    if not os.path.isfile(OAUTH_FILE):
        raise FileNotFoundError(f"Fichier d'auth introuvable : {OAUTH_FILE}\n"
                                f"Tu dois d'abord exécuter 'ytmusicapi oauth' pour générer ce fichier, "
                                f"ou utiliser un headers_auth.json (méthode cookies).")
    ytmusic = YTMusic(OAUTH_FILE)

def handle_music_command(command_text):
    """
    Exemples de commandes :
      "Music, play Nirvana"
      "Music, play album Discovery by Daft Punk"
      "Music, play playlist My Favorite Songs"

    Retourne un dict : { "title", "artist", "videoId", "thumbnail" }
    OU un message d'erreur (str).
    """
    global ytmusic
    if not ytmusic:
        try:
            init_ytmusic()
        except Exception as e:
            return f"Erreur d'initialisation YTMusic : {e}"

    cmd = command_text.lower()
    # Retirer les mots-clés "music"/"musique"/"play"
    for token in ["music", "musique", "play"]:
        cmd = cmd.replace(token, "")
    query = cmd.strip()
    if not query:
        return "❓ Pas de requête musicale détectée."

    # Recherche dans YouTube Music
    results = ytmusic.search(query, filter="songs")
    if not results:
        return f"⚠️ Aucun résultat trouvé pour : {query}"

    track = results[0]
    video_id = track.get("videoId")
    title = track.get("title", "Sans titre")
    artists = track.get("artists", [])
    artist_name = artists[0]["name"] if artists else "Artiste inconnu"

    thumbnails = track.get("thumbnails", [])
    thumbnail_url = thumbnails[-1]["url"] if thumbnails else None

    return {
        "title": title,
        "artist": artist_name,
        "videoId": video_id,
        "thumbnail": thumbnail_url
    }
