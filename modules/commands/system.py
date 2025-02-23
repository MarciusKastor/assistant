
from datetime import datetime
import modules.hue as hue
from modules.voice import speak

def stop_conversation():
    speak("D'accord, j'arrête d'écouter.")
    return "🛑 Conversation arrêtée par commande vocale."

def list_rooms():
    rooms = hue.ROOMS.keys()
    if rooms:
        return f"🏠 Les pièces disponibles sont : {', '.join(rooms)}."
    return "❌ Aucune pièce trouvée."

def get_time():
    return f"🕒 Il est {datetime.now().strftime('%H:%M')}"

def get_weather():
    return "🌤️ Il fait beau aujourd'hui."
