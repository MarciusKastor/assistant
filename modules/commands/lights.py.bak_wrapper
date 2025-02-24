
import modules.hue as hue

def control_lights(action, room=None):
    success = hue.control_lights(action, room)
    if success is None:
        return "❌ Impossible de trouver la pièce spécifiée."
    room_info = f" de {room}" if room else ""
    emoji = "💡"
    return f"{emoji} J'ai {('allumé' if action == 'on' else 'éteint')} les lumières{room_info}."
