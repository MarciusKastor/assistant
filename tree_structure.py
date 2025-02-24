#!/usr/bin/env python3
import os
import sys

def generate_tree(root_dir, prefix=""):
    """
    Parcourt récursivement le répertoire root_dir et génère une chaîne de caractères
    représentant sa structure sous forme d'arbre.
    """
    try:
        entries = os.listdir(root_dir)
    except PermissionError:
        return prefix + "└── [Permission denied]\n"

    entries.sort()
    tree_str = ""
    count = len(entries)
    for i, entry in enumerate(entries):
        full_path = os.path.join(root_dir, entry)
        if i == count - 1:
            connector = "└── "
            extension = "    "
        else:
            connector = "├── "
            extension = "│   "
        tree_str += prefix + connector + entry + "\n"
        if os.path.isdir(full_path):
            tree_str += generate_tree(full_path, prefix + extension)
    return tree_str

if __name__ == "__main__":
    # Le répertoire de départ peut être passé en argument, sinon le répertoire courant est utilisé.
    if len(sys.argv) > 1:
        start_dir = sys.argv[1]
    else:
        start_dir = "."
    
    tree_output = f"{os.path.abspath(start_dir)}\n" + generate_tree(start_dir)
    print(tree_output)
