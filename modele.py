import sqlite3

ma_base_de_donnees = "bdd_site_marchand"

socket = sqlite3.connect(ma_base_de_donnees)
request = socket.cursor()

# création des tables :
request.execute(
    """
        CREATE TABLE IF NOT EXISTS utilisateurs(
        login TEXT PRIMARY KEY UNIQUE,
        mdp TEXT)
    """
                )

