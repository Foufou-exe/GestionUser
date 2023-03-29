"""Fichier principal de l'application"""

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


""" Connexion à la base de données MongoDB"""

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


def update_users_table():
    """Mettre à jour la table des utilisateurs"""
    for user in users_table.get_children():
        users_table.delete(user)

    users = db.users.find({}, {"_id": 0})
    for user in users:
        users_table.insert(
            "", tk.END, values=(user["id"], user["username"], user["password"])
        )


def update_user():
    """Mettre à jour l'utilisateur sélectionné dans la table des utilisateurs"""
    global selected_value, selected_user_id
    if selected_value and selected_user_id:
        new_value = update_entry.get()
        if selected_value == "password":
            db.users.update_one(
                {"id": selected_user_id}, {"$set": {"password": new_value}}
            )
        elif selected_value == "username":
            db.users.update_one(
                {"id": selected_user_id}, {"$set": {"username": new_value}}
            )
        update_users_table()
        update_entry.delete(0, tk.END)


def update_users_table():
    """Mettre à jour la table des utilisateurs"""
    for user in users_table.get_children():
        users_table.delete(user)

    users = db.users.find({}, {"_id": 0})
    for user in users:
        id_value = user["id"]
        username_value = user["username"]
        password_value = mask_password(user["password"])
        users_table.insert(
            "", tk.END, values=(id_value, username_value, password_value)
        )


def mask_password(password):
    """Masquer le mot de passe avec des astérisques"""
    return "*" * len(password)


def get_selected_values(event):
    """Récupérer les valeurs sélectionnées dans la table des utilisateurs"""
    global selected_value, selected_user_id
    try:
        clicked_column = users_table.identify_column(event.x)
        selected_item = users_table.selection()

        if not selected_item:
            selected_value = None
            return

        selected_item = selected_item[0]

        if clicked_column == "#3":  # La colonne "Password" est la 3ème colonne
            id_value = users_table.item(selected_item)["values"][0]
            selected_value = "password"
            selected_user_id = id_value
            password_value = db.users.find_one({"id": id_value})["password"]
            _hash = users_table.item(selected_item)["values"][2]
            if _hash == password_value:
                users_table.item(
                    selected_item,
                    values=(
                        id_value,
                        users_table.item(selected_item)["values"][1],
                        mask_password(password_value),
                    ),
                )
            else:
                users_table.item(
                    selected_item,
                    values=(
                        id_value,
                        users_table.item(selected_item)["values"][1],
                        password_value,
                    ),
                )

        if clicked_column == "#2":
            users_table.item(selected_item)["values"][1]
            id_value = users_table.item(selected_item)["values"][0]
            selected_value = "username"
            selected_user_id = id_value

        if clicked_column == "#1":
            id_value = users_table.item(selected_item)["values"][0]
            selected_user_id = id_value
            
    except IndexError:
        pass


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


if __name__ == "__main__":
    main()
