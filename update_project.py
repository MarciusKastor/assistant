#!/usr/bin/env python3
import shutil

def main():
    webapp_file = "modules/webapp.py"
    backup_file = "modules/webapp.py.bak"

    print("1) Sauvegarde du fichier d'origine...")
    shutil.copyfile(webapp_file, backup_file)

    with open(webapp_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Étape 2 : suppression des lignes entre
    # "answer = generate_answer(question)" et
    # 'return jsonify({"answer": answer, "history": conversation_history})'
    start_index = -1
    end_index = -1

    for i, line in enumerate(lines):
        if "answer = generate_answer(question)" in line:
            start_index = i
        if (
            'return jsonify({"answer": answer, "history": conversation_history})' in line
            and start_index != -1
        ):
            end_index = i
            break

    # Si on a trouvé un bloc à supprimer
    if start_index != -1 and end_index != -1:
        del lines[start_index : end_index + 1]
        print("2) Ancien bloc supprimé.")
    else:
        print("2) Avertissement : bloc à supprimer non trouvé. (Script ne supprime rien.)")

    # Le nouveau bloc de code à insérer
    new_code_block = [
        "        # DEBUT NOUVEAU CODE\n",
        "        raw_answer = generate_answer(question)\n",
        "\n",
        "        if isinstance(raw_answer, tuple):\n",
        "            textual_answer, deezer_url = raw_answer\n",
        "            conversation_history.append({\n",
        "                \"question\": question,\n",
        "                \"answer\": textual_answer,\n",
        "                \"deezer_url\": deezer_url\n",
        "            })\n",
        "            threading.Thread(target=speak, args=(textual_answer,), daemon=True).start()\n",
        "            return jsonify({\n",
        "                \"answer\": textual_answer,\n",
        "                \"deezer_url\": deezer_url,\n",
        "                \"history\": conversation_history\n",
        "            })\n",
        "        else:\n",
        "            answer = raw_answer\n",
        "            conversation_history.append({\"question\": question, \"answer\": answer})\n",
        "            threading.Thread(target=speak, args=(answer,), daemon=True).start()\n",
        "            return jsonify({\n",
        "                \"answer\": answer,\n",
        "                \"history\": conversation_history\n",
        "            })\n",
        "        # FIN NOUVEAU CODE\n",
    ]

    # Étape 3 : insertion du nouveau bloc
    # On cherche la ligne "question = data.get("question", "")" après "if request.method == "POST":"
    insert_index = -1
    in_post_block = False

    for i, line in enumerate(lines):
        if 'if request.method == "POST":' in line:
            in_post_block = True
        if in_post_block and "question = data.get(" in line:
            insert_index = i
            break

    if insert_index == -1:
        print("3) Avertissement : impossible de trouver la ligne question = data.get(...) dans le bloc POST.")
    else:
        # On insère le bloc juste après la ligne `question = data.get(...)`
        insert_index += 1
        for new_line in reversed(new_code_block):
            lines.insert(insert_index, new_line)
        print("3) Nouveau bloc inséré.")

    # On réécrit le fichier
    with open(webapp_file, "w", encoding="utf-8") as f:
        f.writelines(lines)

    print("Terminé. Un backup se trouve dans", backup_file)

if __name__ == "__main__":
    main()
