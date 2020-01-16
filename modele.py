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

# création de mon compte admin:
request.execute(
    """
        INSERT INTO utilisateurs
        SELECT "admin@admin.gege", "46d67f3083f7c097922e45295137d48e0827ca3484bb27749cbeca5743906203"
        WHERE NOT EXISTS (SELECT * FROM utilisateurs WHERE login = 'admin@admin.gege')
    """
)

socket.commit()


class MaBaseDeDonnees:
    def __init__(self):
        ma_base_de_donnees = "ma_base_de_donnees"  # file containing the SQLite Database
        self.socket = sqlite3.connect(ma_base_de_donnees)  # creating connection to the database
        # creating a cursor that will contain the SQL queries to execute
        self.request = self.socket.cursor()

    def verifier_si_compte_existe_deja(self, log, mdp_hashe):
        """ verify if the account with login and password entered is in database. """
        self.request.execute(
            """SELECT count(*) FROM utilisateurs 
               WHERE login = '{}' AND mdp = '{}' """.format(log, mdp_hashe)
        )
        data = self.request.fetchone()[0]
        if data == 0:
            return "denied"
        else:
            return "granted"
