import sqlite3

ma_base_de_donnees = "bdd_site_marchand"

socket = sqlite3.connect(ma_base_de_donnees)
request = socket.cursor()

# création des tables :
request.execute(
    """
        CREATE TABLE IF NOT EXISTS utilisateurs(
        email TEXT PRIMARY KEY UNIQUE,
        mdp TEXT)
    """
)

request.execute(
    """
        CREATE TABLE IF NOT EXISTS administrateurs(
        email TEXT PRIMARY KEY UNIQUE,
        mdp TEXT)
    """
)

# création de mon compte admin:
request.execute(
    """
        INSERT INTO administrateurs
        SELECT "admin@admin.gege", "46d67f3083f7c097922e45295137d48e0827ca3484bb27749cbeca5743906203"
        WHERE NOT EXISTS (SELECT * FROM administrateurs WHERE email = 'admin@admin.gege')
    """
)

# création de mon compte utilisateur:
request.execute(
    """
        INSERT INTO utilisateurs
        SELECT "gege@gege.com", "46d67f3083f7c097922e45295137d48e0827ca3484bb27749cbeca5743906203"
        WHERE NOT EXISTS (SELECT * FROM utilisateurs WHERE email = 'gege@gege.com')
    """
)

socket.commit()


class MaBaseDeDonnees:
    def __init__(self):
        ma_base_de_donnees = "bdd_site_marchand"  # file containing the SQLite Database
        self.socket = sqlite3.connect(ma_base_de_donnees)  # creating connection to the database
        # creating a cursor that will contain the SQL queries to execute
        self.request = self.socket.cursor()

    def verifier_si_compte_utilisateur_existe_deja(self, email, mdp_hashe):
        """ vérifier si le compte avec cet email et mot de passe existe dans la base de données """
        self.request.execute(
            """SELECT count(*) FROM utilisateurs 
               WHERE email = '{}' AND mdp = '{}' """.format(email, mdp_hashe)
        )
        data = self.request.fetchone()[0]
        if data == 0:
            return "faux"
        else:
            return "vrai"

    def verifier_si_compte_administrateur_existe_deja(self, email, mdp_hashe):
        """ vérifier si le compte avec cet email et mot de passe existe dans la base de données """
        self.request.execute(
            """SELECT count(*) FROM administrateurs 
               WHERE email = '{}' AND mdp = '{}' """.format(email, mdp_hashe)
        )
        data = self.request.fetchone()[0]
        if data == 0:
            return "faux"
        else:
            return "vrai"
