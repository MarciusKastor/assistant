import pyttsx3
import platform
import subprocess

def init_voice():
    engine = pyttsx3.init()
    engine.setProperty('rate', 180)  # Vitesse normale
    engine.setProperty('volume', 1.0)
    return engine

def speak(text):
    if platform.system() == "Darwin":  # macOS
        # Voix "Amélie" avec vitesse normale
        subprocess.run(["say", "-v", "Amélie", text])
    else:
        engine = init_voice()
        engine.say(text)
        engine.runAndWait()
