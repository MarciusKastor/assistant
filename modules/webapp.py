from flask import Flask, request, jsonify, render_template, redirect
import modules.commands.lights as lights_cmd
import modules.commands.search as search_cmd
import modules.commands.system as system_cmd
import modules.commands.music as music_cmd  # Ajout des commandes musicales
from modules.hue import ROOMS
import threading
from modules.voice import speak

app = Flask(__name__, template_folder="../templates")
conversation_history = []

def generate_answer(question):
    lower_question = question.lower()

    # 🎤 Commandes système
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

    # 🔎 Recherches avec variantes
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

    # 🎵 Commandes musicales (Deezer)
    music_keywords = [
        "mets de la musique", "joue de la musique", "lance de la musique", "écoute", "mets", "joue", "lance",
        "écoute de la musique", "joue-moi de la musique", "mets une chanson", "lance une chanson", "écouter de la musique"
    ]

    if any(kw in lower_question for kw in music_keywords + ["deezer"]):
        deezer_url, response = music_cmd.get_deezer_embed_url(lower_question)
        return response, deezer_url

    # 💡 Commandes lumières
    if any(word in lower_question for word in ["allume", "allumer", "active", "démarre"]) and "lumière" in lower_question:
        room = next((r for r in ROOMS if r in lower_question), None)
        if room:
            return lights_cmd.control_lights("on", room)
        return f"🚫 Veuillez spécifier une pièce pour allumer les lumières. 🏠 {system_cmd.list_rooms()}"

    if any(word in lower_question for word in ["éteins", "éteindre", "coupe", "désactive"]) and "lumière" in lower_question:
        room = next((r for r in ROOMS if r in lower_question), None)
        if room:
            return lights_cmd.control_lights("off", room)
        return f"🚫 Veuillez spécifier une pièce pour éteindre les lumières. 🏠 {system_cmd.list_rooms()}"

    return "❓ Désolé, je n'ai pas compris votre question."


@app.route("/")
def index():
    return redirect("/ask")

@app.route("/ask", methods=["GET", "POST"])
def ask():
    if request.method == "POST":
        data = request.get_json()
        question = data.get("question", "")
        # DEBUT NOUVEAU CODE
        raw_answer = generate_answer(question)

        if isinstance(raw_answer, tuple):
            textual_answer, deezer_url = raw_answer
            conversation_history.append({
                "question": question,
                "answer": textual_answer,
                "deezer_url": deezer_url
            })
            threading.Thread(target=speak, args=(textual_answer,), daemon=True).start()
            return jsonify({
                "answer": textual_answer,
                "deezer_url": deezer_url,
                "history": conversation_history
            })
        else:
            answer = raw_answer
            conversation_history.append({"question": question, "answer": answer})
            threading.Thread(target=speak, args=(answer,), daemon=True).start()
            return jsonify({
                "answer": answer,
                "history": conversation_history
            })
        # FIN NOUVEAU CODE
    return render_template("chat.html")

def run_app():
    app.run(host="0.0.0.0", port=5001, debug=True)
