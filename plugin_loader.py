#!/usr/bin/env python3
import importlib
import os
import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Répertoire des plugins (modules de commandes)
PLUGINS_DIR = os.path.join(os.path.dirname(__file__), "modules", "commands")
plugins = {}

def load_plugins():
    global plugins
    for filename in os.listdir(PLUGINS_DIR):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = filename[:-3]
            full_module_name = f"modules.commands.{module_name}"
            try:
                module = importlib.import_module(full_module_name)
                plugins[module_name] = module
                print(f"[PLUGIN] Chargé: {full_module_name}")
            except Exception as e:
                print(f"[PLUGIN] Erreur lors du chargement de {full_module_name} : {e}")

class PluginEventHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(".py"):
            filename = os.path.basename(event.src_path)
            module_name = filename[:-3]
            full_module_name = f"modules.commands.{module_name}"
            if module_name in plugins:
                try:
                    plugins[module_name] = importlib.reload(plugins[module_name])
                    print(f"[PLUGIN] Rechargé: {full_module_name}")
                except Exception as e:
                    print(f"[PLUGIN] Erreur lors du rechargement de {full_module_name} : {e}")

if __name__ == "__main__":
    load_plugins()
    event_handler = PluginEventHandler()
    observer = Observer()
    observer.schedule(event_handler, PLUGINS_DIR, recursive=False)
    observer.start()
    print("Surveillance des plugins activée. Appuyez sur Ctrl+C pour arrêter.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
