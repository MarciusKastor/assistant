#!/usr/bin/env python3
import os
import sys

def is_text_file(file_path, blocksize=512):
    """
    Vérifie si un fichier est textuel en lisant un bloc de données.
    Si le bloc contient un octet nul, il est considéré comme binaire.
    """
    try:
        with open(file_path, "rb") as f:
            block = f.read(blocksize)
        return b'\0' not in block
    except Exception:
        return False

def print_file_contents(root_dir):
    """
    Parcourt récursivement le répertoire root_dir et génère une chaîne
    contenant, pour chaque fichier, son chemin relatif et son contenu.
    Les fichiers binaires ne sont pas affichés, mais signalés comme tels.
    """
    output = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in sorted(filenames):
            file_path = os.path.join(dirpath, filename)
            rel_path = os.path.relpath(file_path, root_dir)
            output.append(f"=== {rel_path} ===")
            if is_text_file(file_path):
                try:
                    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                        content = f.read()
                    output.append(content)
                except Exception as e:
                    output.append(f"[Erreur lors de la lecture du fichier: {e}]")
            else:
                output.append("[Fichier binaire, contenu non affiché]")
            output.append("\n" + "="*40 + "\n")
    return "\n".join(output)

if __name__ == "__main__":
    # Si un répertoire est passé en argument, l'utiliser ; sinon, le répertoire courant.
    start_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    result = print_file_contents(start_dir)
    print(result)
