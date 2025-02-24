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
    if room_name:
        room_id = ROOMS.get(room_name.lower())
        if not room_id:
            return False  # Room not found

        url = f"http://{BRIDGE_IP}/api/{USERNAME}/groups/{room_id}/action"
        payload = {"on": state == "on"}
        response = requests.put(url, json=payload)

        if response.status_code == 200:
            return True
    return False