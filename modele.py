import sqlite3

ma_base_de_donnees = "bdd_site_marchand"

socket = sqlite3.connect(ma_base_de_donnees)
request = socket.cursor()

# création des tables :
request.execute(
    """
        CREATE TABLE IF NOT EXISTS utilisateurs(
        id_utilisateur INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        email TEXT NOT NULL UNIQUE,
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
        INSERT INTO utilisateurs (email, mdp, nom, prenom, tel, numero_voie, nom_voie, code_postal, ville)
        SELECT 'gege@gege.com', '46d67f3083f7c097922e45295137d48e0827ca3484bb27749cbeca5743906203', 
        'gege', 'alf', 0600000000, 2, 'rue machinchose', 75011, 'paris'
        WHERE NOT EXISTS (SELECT * FROM utilisateurs WHERE email = 'gege@gege.com')
    """
)

'''
# test ajout d'un produit dans la base de données:
request.execute(
    """
        INSERT INTO produits (prix_produit_unite, categorie , commentaire , lien_photo, en_stock, 
        reapprovisionnement_en_cours, baisse_de_prix, nouveaute)
        VALUES 
            ('3.20', 'Clés USB', "Quand tu fais le calcul, je suis mon meilleur modèle car c'est un très, très gros travail puisque the final conclusion of the spirit is perfection C'est pour ça que j'ai fait des films avec des replicants.", 
            './static/images/4go_noname_cle_usb2.jpg', 1, 0, 0, 0), 
            ('10.99', 'Cartes mémoire', "Mesdames, messieurs, la crise actuelle nous assure à toutes et à tous les moyens d'aller dans le sens d'un processus allant vers plus d'égalité.", 
             './static/images/2go_sandisk_sdcard.png', 1, 0, 0, 1),
            ('10.99', 'Nouveautés et baisses de prix', "Mesdames, messieurs, la crise actuelle nous assure à toutes et à tous les moyens d'aller dans le sens d'un processus allant vers plus d'égalité.", 
            './static/images/2go_sandisk_sdcard.png', 1, 0, 0, 1),
            ('14.99', 'Cartes mémoire', "Le passage latin classique qui ne vieillit jamais, apprécie autant (ou aussi peu) le lorem ipsum que vous pouvez manipuler avec notre générateur de texte de remplissage facile à utiliser.", './static/images/16go_sandisk_sdhc_card.png', 0, 1, 0, 0),
            ('16.99', 'Cartes mémoire', "Si vous n'avez pas vu Game of Thrones, allez le voir tout de suite. Si vous avez alors, vous comprendrez totalement pourquoi ce générateur de lorem ipsum sur le thème de Hodor est tout simplement génial.", 
            './static/images/32go_sandisk_sdhc.jpg', 1, 0, 0, 0),
            ('17.00', 'Cartes mémoire', "Le Hipster Ipsum est une version artisanale et artisanale du petit générateur classique de lipsem ipsum, qui donnera à vos mocks une touche bleue.", 
            './static/images/64go_noname_sdxc.jpg', 1, 0, 15, 0),
            ('17.00', 'Nouveautés et baisses de prix', "Le Hipster Ipsum est une version artisanale et artisanale du petit générateur classique de lipsem ipsum, qui donnera à vos mocks une touche bleue.", 
            './static/images/64go_noname_sdxc.jpg', 1, 0, 15, 0),
            ('32.50', 'Cartes mémoire', "Si vous ne lisez pas Twitter, les nouvelles, ou si vous ne pouvez pas obtenir assez de l'oraison légendaire de l'apprenti hôte, essayez ce générateur Trump lorem ipsum  pour la taille.", 
            './static/images/128go_sandisk_extreme.png', 1, 0, 0, 0),
            ('42.70', 'Cartes mémoire', "Comme votre lorem ipsum extra croustillant? Ensuite, Bacon Ipsum est le générateur de texte d'espace réservé pour vous. Le côté des oeufs et des hashbrowns est facultatif, mais recommandé.", 
            './static/images/128go_sandisk_sdxc_extremepro.jpg', 1, 0, 10, 0),
            ('42.70', 'Nouveautés et baisses de prix', "Comme votre lorem ipsum extra croustillant? Ensuite, Bacon Ipsum est le générateur de texte d'espace réservé pour vous. Le côté des oeufs et des hashbrowns est facultatif, mais recommandé.", 
            './static/images/128go_sandisk_sdxc_extremepro.jpg', 1, 0, 10, 0),
            ('12.99', 'Clés USB', "Soulevez votre conception des morts avec une armée de Zombie Ipsum, texte de remplissage effrayant qui ne mourra pas. Essayez le lorem ipsum des morts-vivants si vous osez...", 
            './static/images/32go_sandisk_cle_usb3.webp', 1, 0, 0, 0),
            ('7.99', 'Clés USB', "Explorez les contrées lointaines de la galaxie avec ce générateur de texte fictif sur le thème de l'espace, avec des citations de classiques TV comme Star Trek et de vrais astronautes eux-mêmes.", 
            './static/images/16go_dtse_cle_usb2.webp', 0, 1, 0, 0),
            ('45.12', 'Clés USB', "Tu vois, premièrement, il faut se recréer... pour recréer... a better you et ça, c'est très dur, et, et, et... c'est très facile en même temps. C'est pour ça que j'ai fait des films avec des replicants.", 
            './static/images/128go_sandisk_cle_usb3.webp', 1, 0, 0, 1),
            ('45.12', 'Nouveautés et baisses de prix', "Tu vois, premièrement, il faut se recréer... pour recréer... a better you et ça, c'est très dur, et, et, et... c'est très facile en même temps. C'est pour ça que j'ai fait des films avec des replicants.", 
            './static/images/128go_sandisk_cle_usb3.webp', 1, 0, 0, 1),
            ('32.45', 'SSD', "Riche en fibres et bon pour votre cœur, Veggie Ipsum livre le texte le plus organique, cueilli à la main, lorem ipsum placeholder à votre porte (ou navigateur... je suppose).", 
            './static/images/120go_samsung_ssd.webp', 1, 0, 0, 0),
            ('59.99', 'SSD', "Sentez comme un vrai meathead dans vos maquettes avec Bro Ipsum, spécialisé dans un lorem ipsum composé de phrases-clés tendrement déployées dans la plus terne des conversations.", 
            './static/images/240go_crucial_ssd.webp', 1, 0, 0, 0),
            ('38.55', 'HDD', "You see, je suis mon meilleur modèle car il faut se recréer... pour recréer... a better you et je ne cherche pas ici à mettre un point ! Donc on n'est jamais seul spirituellement !", 
            './static/images/1to_maxtor_hdd.jfif', 1, 0, 0, 0),
            ('62.00', 'HDD', "Très chers compatriotes, vous le savez et je vous le redit que la prise de conscience de nos dirigeants a pour conséquence obligatoire l'urgente nécessité d'un processus allant vers plus d'égalité.", 
            './static/images/2to_wd-hdd.jfif', 1, 0, 0, 0),            
            ('22.99', 'HDD', "Je me souviens en fait, après il faut s'intégrer tout ça dans les environnements et il faut se recréer... pour recréer... a better you parce que spirituellement, on est tous ensemble, ok ?", 
            './static/images/500go_samsung_hdd.jfif', 0, 1, 0, 1),
            ('59.20', 'HDD', "Ces feuilles de lettrage pourraient être frottées sur n'importe où et ont été rapidement adoptés par les graphistes, les imprimeurs, les architectes et les annonceurs pour leur aspect professionnel et la facilité d'utilisation.", 
            './static/images/3to_noname_hdd.jfif', 1, 0, 50, 0),
            ('59.20', 'Nouveautés et baisses de prix', "Ces feuilles de lettrage pourraient être frottées sur n'importe où et ont été rapidement adoptés par les graphistes, les imprimeurs, les architectes et les annonceurs pour leur aspect professionnel et la facilité d'utilisation.",
            './static/images/3to_noname_hdd.jfif', 1, 0, 50, 0),
            ('9.99', 'RAM', "Tu comprends, je sais que, grâce à ma propre vérité c'est un très, très gros travail et c'est très, très beau d'avoir son propre moi-même ! Ça respire le meuble de Provence, hein ?", 
            './static/images/2go_kingston_ram.jfif', 0, 1, 0, 0),
            ('7.10', 'RAM', "Loin, très loin, au delà des monts Mots, à mille lieues des pays Voyellie et Consonnia, demeurent les Bolos Bolos. Ils vivent en retrait, à Bourg-en-Lettres, sur les côtes de la Sémantique, un vaste océan de langues.", 
            './static/images/1go_noname_ram.jfif', 1, 0, 0, 0),
            ('89.99', 'RAM', "La liberté ne tiens qu'à un fils et c'est pourquoi je tiens à vous dire que la crise actuelle doit s'intégrer à la finalisation globale d'un rappel des droits fondamentaux de notre pays", 
            './static/images/8gox4_gskill_ram.jfif', 1, 0, 25, 0),
            ('89.99', 'Nouveautés et baisses de prix', "La liberté ne tiens qu'à un fils et c'est pourquoi je tiens à vous dire que la crise actuelle doit s'intégrer à la finalisation globale d'un rappel des droits fondamentaux de notre pays", 
            './static/images/8gox4_gskill_ram.jfif', 1, 0, 25, 0)
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

    def trouver_id_utilisateur(self, email, mdp_hashe):
        """               """
        self.request.execute(
            """SELECT id_utilisateur FROM utilisateurs 
               WHERE email = '{}' AND mdp = '{}' """.format(email, mdp_hashe)
        )
        data = self.request.fetchone()[0]
        print(data)
        return data

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
                reapprovisionnement_en_cours, baisse_de_prix, nouveaute, numero_produit 
                from produits WHERE categorie = '{}' """.format(liste_categories[i])
            )
            data[liste_categories[i]] = self.request.fetchall()
        return data
