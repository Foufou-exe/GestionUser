# GestionUser

## Description ✨

Ce programme est une application de gestion des utilisateurs utilisant Tkinter et MongoDB. Il permet d'ajouter, de supprimer et de mettre à jour les utilisateurs avec leur mot de passe.

## Prérequis ❓

- Python 3
- Tkinter
- ttkbootstrap
- pymongo

## Fonctionnalités 🚀

- Ajouter un nouvel utilisateur avec un mot de passe aléatoire
- Supprimer un utilisateur sélectionné
- Mettre à jour le nom d'utilisateur ou le mot de passe d'un utilisateur sélectionné
- Masquer les mots de passe avec des astérisques dans la table des utilisateurs

## Utilisation 👨‍💻

Clonez ou téléchargez ce dépôt :

```cmd
git clone https://github.com/Foufou-exe/GestionUser
```

Installez les dépendances en exécutant :

```python
pip install -r requirements.txt
```

Exécutez le fichier gestionUser.py :

```cmd
python gestionUser.py
```

### Exemple utilisation ✨

![screen2](images/screen2.gif)
## Interface utilisateur👌

L'interface utilisateur comprend :

- Un champ de saisie pour le nom d'utilisateur
- Un bouton "Ajouter" pour ajouter un nouvel utilisateur
- Un bouton "Supprimer" pour supprimer l'utilisateur sélectionné
- Un champ de saisie pour la valeur à mettre à jour (nom d'utilisateur ou mot de passe)
- Un bouton "Mettre à jour" pour mettre à jour la valeur sélectionnée
- Une table affichant les utilisateurs avec leurs ID, noms d'utilisateur et mots de passe masqués

### Visuel GestionUser

![Screen](images/screen.png)

## Code

Le code principal est divisé en plusieurs fonctions pour gérer les différentes fonctionnalités de l'application :

- `add_user()` : ajoute un nouvel utilisateur à la base de données avec un mot de passe aléatoire.

- `delete_user()` : supprime l'utilisateur sélectionné dans la table des utilisateurs.

- `update_users_table()` : met à jour la table des utilisateurs avec les données de la base de données.

- `update_user()` : met à jour l'utilisateur sélectionné dans la table des utilisateurs (nom d'utilisateur ou mot de passe).
mask_password(password): masque le mot de passe avec des astérisques.
get_selected_values(event): récupère les valeurs sélectionnées dans la table des utilisateurs lorsqu'un utilisateur clique sur une cellule de la table.

- `main()` : fonction principale qui gère l'interface utilisateur et les interactions utilisateur.

## Structure du code

Le code est structuré de la manière suivante :

- Importation des modules nécessaires

```python
# Importer les modules
import tkinter as tk
from tkinter import *
from ttkbootstrap import *
import tkinter.ttk as ttk
import random
import string
import os
import platform
import sys
from pymongo import MongoClient
```

- Connexion à la base de données MongoDB et création de la collection "users" si elle n'existe pas

```python
uri = "mongodb://localhost:27017"

client = MongoClient(uri)

db = client["test"]

validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["username", "password"],
        "properties": {
            "id": {"bsonType": "int"},
            "username": {"bsonType": "string"},
            "password": {"bsonType": "string"},
        },
    }
}

if "users" not in db.list_collection_names():
    db.create_collection("users", validator=validator)
```

- Définition des fonctions pour gérer les fonctionnalités de l'application

```python
def add_user():
    """Ajouter un nouvel utilisateur à la base de données"""
    name = user_entry.get()
    if name:
        # Récupérer l'ID du dernier utilisateur ajouté
        last_user = db.users.find().sort("id", -1).limit(1)
        last_id = 0
        for user in last_user:
            last_id = user["id"]

        # Extraire le numéro à partir de l'ID et l'incrémenter
        new_num = last_id + 1

        # Générer un mot de passe aléatoire
        password = "".join(random.choices(string.ascii_letters + string.digits, k=8))

        # Insérer un nouveau document utilisateur dans la collection
        db.users.insert_one({"id": new_num, "username": name, "password": password})

        update_users_table()
        user_entry.delete(0, tk.END)

def delete_user():
    """Supprimer l'utilisateur sélectionné dans la table des utilisateurs"""
    selected_user = users_table.item(users_table.selection())["values"][0]
    db.users.delete_one({"id": selected_user})
    update_users_table()

```

- Définition de la fonction principale main() qui gère l'interface utilisateur et les interactions utilisateur

```python
def main():
    """Fonction principale"""
    global users_table, update_entry, user_entry
    try:
        root = tk.Tk()
        root.theme = Style(theme="superhero")
        root.title("Gestion des utilisateurs")
        root.geometry("1280x720")

        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)

        chemin_python = os.path.abspath(__file__)

        repertoire_travail = os.path.dirname(chemin_python)
        if platform.system() == "Windows":
            file_path_icon3 = os.path.join(repertoire_travail, "images/code.ico")
            root.iconbitmap(root, default=file_path_icon3)
        else:
            file_path_icon3 = os.path.join(repertoire_travail, "images/code.png")
            root.iconphoto(root, default=PhotoImage(file=file_path_icon3))

        frame = ttk.Frame(root, padding=10)
        frame.grid(row=0, column=0, sticky=tk.NSEW)

        for i in range(4):
            frame.grid_columnconfigure(i, weight=1)
        frame.grid_rowconfigure(1, weight=1)

        user_label = ttk.Label(frame, text="Nom d'utilisateur :")
        user_label.grid(row=0, column=0, padx=(0, 10), sticky=tk.W)

        user_entry = ttk.Entry(frame)
        user_entry.grid(row=0, column=0, padx=(110, 10), sticky=tk.W)

        add_button = ttk.Button(frame, text="Ajouter", command=add_user)
        add_button.grid(row=0, column=0, padx=(250, 0), sticky=tk.W)

        delete_button = ttk.Button(frame, text="Supprimer", command=delete_user)
        delete_button.grid(row=0, column=0, padx=(320, 0), sticky=tk.W)

        update_label = ttk.Label(frame, text="Valeur à mettre à jour :")
        update_label.grid(row=0, column=1, padx=(0, 10), sticky=tk.W)

        update_entry = ttk.Entry(frame)
        update_entry.grid(row=0, column=1, padx=(130, 10), sticky=tk.W)

        update_button = ttk.Button(frame, text="Mettre à jour", command=update_user)
        update_button.grid(row=0, column=1, padx=(270, 0), pady=(0, 0), sticky=tk.W)

        users_table = ttk.Treeview(
            frame,
            columns=("ID", "Username", "Password"),
            show="headings",
        )
        users_table.heading("ID", text="ID")
        users_table.heading("Username", text="Nom d'utilisateur")
        users_table.heading("Password", text="Mot de passe")
        users_table.column("ID", width=100, anchor=tk.CENTER)
        users_table.column("Username", width=200, anchor=tk.CENTER)
        users_table.column("Password", width=300, anchor=tk.CENTER)
        users_table.grid(row=1, column=0, columnspan=4, pady=(10, 0), sticky=tk.NSEW)
        users_table.bind("<Button-1>", get_selected_values)

        update_users_table()
    except Exception(KeyboardInterrupt, SystemExit):
        root.destroy()
        sys.exit(0)
    root.mainloop()
```

- Exécution de la fonction principale main() si le fichier est exécuté en tant que script principal

```python
if __name__ == "__main__":
    main()
```
## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.