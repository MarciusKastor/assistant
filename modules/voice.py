import pyttsx3
import platform
import subprocess

import re

def remove_emojis(text):
    """
    Supprime les émojis du texte afin qu'ils ne soient pas prononcés.
    """
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symboles & pictogrammes
                               u"\U0001F680-\U0001F6FF"  # transport & symboles
                               u"\U0001F1E0-\U0001F1FF"  # drapeaux
                               u"\U00002700-\U000027BF"
                               u"\U000024C2-\U0001F251"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

def init_voice():
    engine = pyttsx3.init()
    engine.setProperty('rate', 180)  # Vitesse normale
    engine.setProperty('volume', 1.0)
    return engine

def speak(text):
    clean_text = remove_emojis(text)
    import platform
    import subprocess
    if platform.system() == "Darwin":
        # Utilise la synthèse vocale de macOS (ici avec la voix "Amélie")
        subprocess.run(["say", "-v", "Amélie", clean_text])
    else:
        import pyttsx3
        engine = pyttsx3.init()
        engine.say(clean_text)
        engine.runAndWait()
def process_command(command_text):
    command_text = command_text.lower()
    if "music" in command_text or "musique" in command_text:
        from modules.commands.music import handle_music_command
        return handle_music_command(command_text)
    else:
        return "❓ Désolé, je n'ai pas compris votre question."

