import sqlite3

ma_base_de_donnees = "bdd_site_marchand"

socket = sqlite3.connect(ma_base_de_donnees)
request = socket.cursor()

# création des tables :
request.execute(
    """
        CREATE TABLE IF NOT EXISTS utilisateurs(
        email TEXT NOT NULL PRIMARY KEY UNIQUE,
        mdp TEXT NOT NULL,
        nom TEXT NOT NULL,
        prenom TEXT NOT NULL,
        tel INT NOT NULL,
        numero_voie TEXT,
        nom_voie TEXT NOT NULL,
        code_postal INT NOT NULL,
        ville TEXT NOT NULL
        )
    """
)

request.execute(
    """
        CREATE TABLE IF NOT EXISTS administrateurs(
        email TEXT NOT NULL PRIMARY KEY UNIQUE,
        mdp TEXT NOT NULL
        )
    """
)

request.execute(
    """
        CREATE TABLE IF NOT EXISTS ventes(
        numero_vente INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        date_vente DATE NOT NULL,
        montant_vente NUM NOT NULL,
        email TEXT,
        FOREIGN KEY (email) REFERENCES utilisateurs(email)
        )
    """
)

request.execute(
    """
        CREATE TABLE IF NOT EXISTS produits(
        numero_produit INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        prix_produit_unite NUM NOT NULL,
        categorie TEXT NOT NULL,
        commentaire TEXT NOT NULL,
        lien_photo TEXT NOT NULL,
        en_stock NUMERIC DEFAULT 1,
        reapprovisionnement_en_cours NUMERIC DEFAULT 0,
        baisse_de_prix NUMERIC DEFAULT 0,
        nouveaute NUMERIC DEFAULT 1        
        )
    """
)

request.execute(
    """
        CREATE TABLE IF NOT EXISTS produits_vendus(
        numero_produit_vendu  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        quantite_produit INT NOT NULL,
        numero_vente INTEGER,
        numero_produit INTEGER,
        FOREIGN KEY (numero_vente) REFERENCES ventes(numero_vente),
        FOREIGN KEY (numero_produit) REFERENCES produits(numero_produit)
        )
    """
)

# création de mon compte admin:
request.execute(
    """
        INSERT INTO administrateurs
        SELECT 'admin@admin.gege', '46d67f3083f7c097922e45295137d48e0827ca3484bb27749cbeca5743906203'
        WHERE NOT EXISTS (SELECT * FROM administrateurs WHERE email = 'admin@admin.gege')
    """
)

# création de mon compte utilisateur:
request.execute(
    """
        INSERT INTO utilisateurs
        SELECT 'gege@gege.com', '46d67f3083f7c097922e45295137d48e0827ca3484bb27749cbeca5743906203', 
        'gege', 'alf', 0600000000, 2, 'rue machinchose', 75011, 'paris'
        WHERE NOT EXISTS (SELECT * FROM utilisateurs WHERE email = 'gege@gege.com')
    """
)

'''
# test ajout d'un produit dans la base de données:
request.execute(
    """
        INSERT INTO produits (prix_produit_unite, categorie ,
        commentaire , lien_photo)
        VALUES ('3.20', 'Clés USB', 'pour tester', './static/images/4go_noname_cle_usb2.jpg'), 
            ('10.99', 'Cartes mémoire', 'pour tester', './static/images/2go_sandisk_sdcard.png'),
            ('10.99', 'Nouveautés et baisses de prix', 'pour tester', './static/images/2go_sandisk_sdcard.png'),
            ('14.99', 'Cartes mémoire', 'pour tester', './static/images/16go_sandisk_sdhc_card.png'),
            ('16.99', 'Cartes mémoire', 'pour tester', './static/images/32go_sandisk_sdhc.jpg'),
            ('17.00', 'Cartes mémoire', 'pour tester', './static/images/64go_noname_sdxc.jpg'),
            ('17.00', 'Nouveautés et baisses de prix', 'pour tester', './static/images/64go_noname_sdxc.jpg'),
            ('32.50', 'Cartes mémoire', 'pour tester', './static/images/128go_sandisk_extreme.png'),
            ('42.70', 'Cartes mémoire', 'pour tester', './static/images/128go_sandisk_sdxc_extremepro.jpg'),
            ('42.70', 'Nouveautés et baisses de prix', 'pour tester', './static/images/128go_sandisk_sdxc_extremepro.jpg'),
            ('12.99', 'Clés USB', 'pour tester', './static/images/32go_sandisk_cle_usb3.webp'),
            ('7.99', 'Clés USB', 'pour tester', './static/images/16go_dtse_cle_usb2.webp'),
            ('45.12', 'Clés USB', 'pour tester', './static/images/128go_sandisk_cle_usb3.webp'),
            ('45.12', 'Nouveautés et baisses de prix', 'pour tester', './static/images/128go_sandisk_cle_usb3.webp'),
            ('32.45', 'SSD', 'pour tester', './static/images/120go_samsung_ssd.webp'),
            ('59.99', 'SSD', 'pour tester', './static/images/240go_crucial_ssd.webp'),
            ('38.55', 'HDD', 'pour tester', './static/images/1to_maxtor_hdd.jfif'),
            ('62.00', 'HDD', 'pour tester', './static/images/2to_wd-hdd.jfif'),
            ('59.20', 'HDD', 'pour tester', './static/images/3to_noname_hdd.jfif'),
            ('22.99', 'HDD', 'pour tester', './static/images/500go_samsung_hdd.jfif'),
            ('59.20', 'Nouveautés et baisses de prix', 'pour tester', './static/images/3to_noname_hdd.jfif'),
            ('9.99', 'RAM', 'pour tester', './static/images/2go_kingston_ram.jfif'),
            ('7.10', 'RAM', 'pour tester', './static/images/1go_noname_ram.jfif'),
            ('89.99', 'RAM', 'pour tester', './static/images/8gox4_gskill_ram.jfif')     
    """
)
'''

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

    def trouver_nom_prenom_utilisateur(self, email, mdp_hashe):
        """               """
        self.request.execute(
            """SELECT nom, prenom FROM utilisateurs 
               WHERE email = '{}' AND mdp = '{}' """.format(email, mdp_hashe)
        )
        data = self.request.fetchone()
        return data[1] + " " + data[0][0].upper() + "."

    def verifier_email(self, email_utilisateur):
        """               """
        self.request.execute(
            """SELECT count(*) FROM utilisateurs 
               WHERE email = '{}' """.format(email_utilisateur)
        )
        data = self.request.fetchone()[0]
        if data == 0:
            return False
        else:
            return True

    def ajouter_utilisateur(self, utilisateur):
        """               """
        self.request.execute(
            """INSERT INTO utilisateurs (email, mdp, nom, prenom, tel, numero_voie, nom_voie,
             code_postal, ville) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')""".format(
                utilisateur[0], utilisateur[1], utilisateur[2],
                utilisateur[3], utilisateur[4], utilisateur[5],
                utilisateur[6], utilisateur[7], utilisateur[8])
        )
        self.socket.commit()

    def recuperer_liste_produits(self, liste_categories):
        """               """
        data = {}
        for i in range(0, len(liste_categories)):
            self.request.execute(
                """SELECT prix_produit_unite, commentaire, lien_photo, en_stock,
                reapprovisionnement_en_cours, baisse_de_prix, nouveaute 
                from produits WHERE categorie = '{}' """.format(liste_categories[i])
            )
            data[liste_categories[i]] = self.request.fetchall()
        print(data)
        return data
