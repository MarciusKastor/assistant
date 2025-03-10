import requests

BRIDGE_IP = "192.168.1.130"
USERNAME = "W1dDORGOqm9ZWMggEbtgJSBDzLHzfn3nduyZnJkS"

ROOMS = {
    "marco": 1,
    "qg": 81,
    "profiler": 201,
    "marco gaiming": 200,
}

def control_lights(state: str, room_name: str = None):
    import requests
    if room_name:
        room_id = ROOMS.get(room_name.lower())
        if not room_id:
            return False  # Pièce introuvable

        # Vérifier l'état actuel via une requête GET
        get_url = f"http://{BRIDGE_IP}/api/{USERNAME}/groups/{room_id}"
        get_response = requests.get(get_url)
        if get_response.status_code == 200:
            current_state = get_response.json().get("action", {}).get("on")
            try:
                # Convertir current_state en booléen (pour gérer par exemple "true"/"false" en chaîne)
                if isinstance(current_state, bool):
                    current_state_bool = current_state
                else:
                    current_state_bool = str(current_state).lower() == "true"
            except Exception:
                current_state_bool = False
            desired_state = (state == "on")
            if current_state_bool == desired_state:
                return "already"

        # Changer l'état de la lumière
        url = f"http://{BRIDGE_IP}/api/{USERNAME}/groups/{room_id}/action"
        payload = {"on": state == "on"}
        response = requests.put(url, json=payload)
        if response.status_code == 200:
            return True
    return False
