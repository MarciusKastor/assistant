from modules.commands.lights import control_lights as lights_control
import modules.commands.search as search_cmd
import modules.commands.system as system_cmd
from modules.hue import ROOMS

def dispatch(question):
    lower_question = question.lower().strip()
    # --- Commande spéciale "Amélie" pour recherche avec résumé
    if lower_question.startswith("amélie "):
        query = lower_question[len("amélie "):].strip()
        from modules.commands.search_with_summary import open_google_search_with_summary
        return open_google_search_with_summary(query)
    # --- Commande spéciale "arthena" pour activer la recherche Google avec résumé
    if lower_question.startswith("arthena "):
        query = lower_question[len("arthena "):].strip()
        from modules.commands.search import open_google_search_with_summary
        return open_google_search_with_summary(query)


    # --- Recherche YouTube (prioritaire)
    youtube_keywords = [
        "cherche sur youtube", "recherche youtube", "montre-moi sur youtube"
    ]
    if any(kw in lower_question for kw in youtube_keywords):
        query = search_cmd.clean_search_query(lower_question, youtube_keywords)
        return search_cmd.open_youtube_search(query)

    # --- Recherche Google par défaut : commande qui commence par "cherche "
    if lower_question.startswith("cherche "):
        query = search_cmd.clean_search_query(lower_question, ["cherche"])
        return search_cmd.open_google_search(query)

    # --- Commandes système (heure, météo, etc.)
    if "heure" in lower_question:
        return system_cmd.get_time()
    if "météo" in lower_question or "temps" in lower_question:
        return system_cmd.get_weather()
    # Optionnel : liste des pièces si la commande contient "pièces" ou "liste"
    room_list_keywords = [
        "quelles sont les pièces", "liste des pièces", "quels sont les pièces",
        "montre-moi les pièces", "donne-moi la liste des pièces", "pièces disponibles",
        "montre les pièces", "affiche les pièces", "dis-moi les pièces"
    ]
    if any(kw in lower_question for kw in room_list_keywords):
        return system_cmd.list_rooms()
    if any(cmd in lower_question for cmd in ["arrête-toi", "stop", "termine la conversation", "cesse d'écouter"]):
        return system_cmd.stop_conversation()

    # --- Commandes pour les lumières
    # Allumer
    if "lumière" in lower_question and any(word in lower_question for word in ["allume", "allumer", "active", "démarre"]):
        room = next((r for r in ROOMS if r in lower_question), None)
        if room:
            result = lights_control("on", room)
            if result == "already":
                return f"💡 Les lumières de la pièce {room} sont déjà allumées."
            elif result:
                return f"💡 La lumière de la pièce {room} a été allumée."
            else:
                return "❌ Une erreur est survenue lors de l'allumage de la lumière."
        else:
            # Si aucune pièce n'est spécifiée, appliquer l'action à toutes les lumières
            results = {r: lights_control("on", r) for r in ROOMS.keys()}
            if all(v == "already" for v in results.values()):
                return "💡 Toutes les lumières sont déjà allumées."
            elif all(v in [True, "already"] for v in results.values()):
                return "💡 Toutes les lumières ont été allumées."
            else:
                return "❌ Une erreur est survenue lors de l'allumage de toutes les lumières."

    # Éteindre
    if "lumière" in lower_question and any(word in lower_question for word in ["éteins", "éteindre", "coupe", "désactive"]):
        room = next((r for r in ROOMS if r in lower_question), None)
        if room:
            result = lights_control("off", room)
            if result == "already":
                return f"💡 Les lumières de la pièce {room} sont déjà éteintes."
            elif result:
                return f"💡 La lumière de la pièce {room} a été éteinte."
            else:
                return "❌ Une erreur est survenue lors de l'extinction de la lumière."
        else:
            # Si aucune pièce n'est spécifiée, appliquer l'action à toutes les lumières
            results = [lights_control("off", r) for r in ROOMS.keys()]
            if all(results):
                return "💡 Toutes les lumières ont été éteintes."
            else:
                return "❌ Une erreur est survenue lors de l'extinction de toutes les lumières."

    # --- Aucune commande reconnue : ne rien renvoyer
    return ""
