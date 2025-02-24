#!/usr/bin/env python3
import os
import re
import sys

# 1. Créer/mettre à jour le module dispatcher.py dans le dossier modules.
dispatcher_content = '''\
from modules.commands.lights import control_lights as lights_control
import modules.commands.search as search_cmd
import modules.commands.system as system_cmd
from modules.hue import ROOMS

def dispatch(question):
    lower_question = question.lower()
    
    # Commandes système
    stop_commands = ["arrête-toi", "stop", "arrête", "termine la conversation", "cesse d'écouter"]
    room_list_commands = [
        "quelles sont les pièces", "liste des pièces", "quels sont les pièces", "montre-moi les pièces",
        "donne-moi la liste des pièces", "peux-tu me montrer les pièces", "pièces disponibles",
        "montre les pièces", "affiche les pièces", "dis-moi les pièces"
    ]
    if any(cmd in lower_question for cmd in stop_commands):
        return system_cmd.stop_conversation()
    if any(kw in lower_question for kw in room_list_commands):
        return system_cmd.list_rooms()
    if "heure" in lower_question:
        return system_cmd.get_time()
    if "météo" in lower_question or "temps" in lower_question:
        return system_cmd.get_weather()

    # Recherches (YouTube / Google)
    youtube_keywords = [
        "cherche sur youtube", "recherche sur youtube", "peux-tu chercher sur youtube",
        "trouve sur youtube", "montre-moi sur youtube", "recherche youtube", "sur youtube"
    ]
    google_keywords = [
        "cherche", "recherche", "cherche-moi", "cherche sur google", "trouve", "peux-tu chercher",
        "peux-tu rechercher", "fais une recherche"
    ]
    if any(kw in lower_question for kw in youtube_keywords):
        query = search_cmd.clean_search_query(lower_question, youtube_keywords)
        return search_cmd.open_youtube_search(query)
    if any(kw in lower_question for kw in google_keywords):
        query = search_cmd.clean_search_query(lower_question, google_keywords)
        return search_cmd.open_google_search(query)

    # Commandes lumières pour allumer
    if any(word in lower_question for word in ["allume", "allumer", "active", "démarre"]) and "lumière" in lower_question:
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
            results = {}
            for r in ROOMS.keys():
                res = lights_control("on", r)
                results[r] = res
            if all(v == "already" for v in results.values()):
                return "💡 Toutes les lumières sont déjà allumées."
            elif all(v in [True, "already"] for v in results.values()):
                return "💡 Toutes les lumières ont été allumées."
            else:
                return "❌ Une erreur est survenue lors de l'allumage de toutes les lumières."

    # Commandes lumières pour éteindre
    if any(word in lower_question for word in ["éteins", "éteindre", "coupe", "désactive"]) and "lumière" in lower_question:
        room = next((r for r in ROOMS if r in lower_question), None)
        if room is None:
            results = []
            for r in ROOMS.keys():
                result = lights_control("off", r)
                results.append(result)
            if all(results):
                return "💡 Toutes les lumières ont été éteintes."
            else:
                return "❌ Une erreur est survenue lors de l'extinction de toutes les lumières."
        else:
            return lights_control("off", room)

    return "❓ Désolé, je n'ai pas compris votre question."
'''

dispatcher_path = os.path.join("modules", "dispatcher.py")
try:
    with open(dispatcher_path, "w", encoding="utf-8") as f:
        f.write(dispatcher_content)
    print(f"[dispatcher.py] Fichier créé/mis à jour : {dispatcher_path}")
except Exception as e:
    print(f"Erreur lors de l'écriture de {dispatcher_path}: {e}")
    sys.exit(1)

# 2. Mettre à jour la fonction generate_answer dans modules/webapp.py pour utiliser le dispatcher.
webapp_path = os.path.join("modules", "webapp.py")
try:
    with open(webapp_path, "r", encoding="utf-8") as f:
        webapp_content = f.read()
except Exception as e:
    print(f"Erreur lors de la lecture de {webapp_path}: {e}")
    sys.exit(1)

# On remplace la définition de generate_answer par une version simplifiée
new_generate_answer = '''\
def generate_answer(question):
    from modules import dispatcher
    return dispatcher.dispatch(question)
'''

# Utilisons une regex pour remplacer la fonction generate_answer existante
pattern = re.compile(r"def generate_answer\(question\):.*?(?=\n@|\nif __name__ == \"__main__\")", re.DOTALL)
new_webapp_content, count = pattern.subn(new_generate_answer, webapp_content)
if count == 0:
    print("La fonction generate_answer n'a pas été trouvée pour mise à jour dans webapp.py.")
    sys.exit(1)

# Sauvegarde du fichier original
backup_webapp = webapp_path + ".bak_refactor"
try:
    with open(backup_webapp, "w", encoding="utf-8") as f_backup:
        f_backup.write(webapp_content)
    print(f"[webapp.py] Sauvegarde réalisée dans {backup_webapp}")
except Exception as e:
    print(f"Erreur lors de la sauvegarde de {webapp_path}: {e}")
    sys.exit(1)

try:
    with open(webapp_path, "w", encoding="utf-8") as f:
        f.write(new_webapp_content)
    print(f"[webapp.py] La fonction generate_answer a été mise à jour dans {webapp_path}")
except Exception as e:
    print(f"Erreur lors de l'écriture de {webapp_path}: {e}")
    sys.exit(1)

print("Refactorisation terminée. Vous pouvez désormais ajouter/modifier des commandes dans modules/dispatcher.py sans toucher à webapp.py.")
sys.exit(0)
