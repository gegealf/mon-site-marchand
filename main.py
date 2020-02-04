#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask  # pip install flask
from os import path
import logging.config
import logging

# pour le fichier de config :
log_file_path = path.join(path.dirname(path.abspath(__file__)), 'log.config')
logging.config.fileConfig(log_file_path)
log = logging.getLogger(__name__)  # définition du logger pour la classe courante

app = Flask(__name__)
app.config['SECRET_KEY'] = "tandiS_quE_leS_crachatS_rougeS"

if __name__ == "__main__":  # python main.py
    import controleur

    app.add_url_rule('/', 'page_d_accueil', view_func=controleur.page_d_accueil)
    app.add_url_rule('/page_d_authentification', 'page_d_authentification', methods=['GET', 'POST'],
                     view_func=controleur.page_d_authentification)
    app.add_url_rule('/page_administrateur', 'page_administrateur', view_func=controleur.page_administrateur)
    app.add_url_rule('/page_creation_compte_utilisateur', 'page_creation_compte_utilisateur', methods=['GET', 'POST'],
                     view_func=controleur.page_creation_compte_utilisateur)
    app.add_url_rule('/deconnexion', 'deconnexion', view_func=controleur.deconnexion)
    app.add_url_rule('/page_fiche_produit/<int:numero_produit>', 'page_fiche_produit',
                     view_func=controleur.page_fiche_produit)
    app.add_url_rule('/page_d_accueil/ajouter_au_panier/<int:numero_produit>', 'page_d_accueil/ajouter_au_panier',
                     view_func=controleur.ajouter_au_panier)
    app.add_url_rule('/page_fiche_produit/<int:numero_produit>/ajouter_au_panier',
                     'page_fiche_produit/ajouter_au_panier', view_func=controleur.ajouter_au_panier)
    app.add_url_rule('/page_panier', 'page_panier', view_func=controleur.page_panier)
    app.add_url_rule('/page_panier/<int:numero_produit>/supprimer_du_panier', 'page_panier/supprimer_du_panier',
                     view_func=controleur.supprimer_du_panier)

    try:
        log.info('démarrage de l\'application')
        SESSION_COOKIE_DOMAIN = '127.0.0.1'
        app.run(host='127.0.0.1', port=8000)  # lancement de l'application en local

        # app.run(host='0.0.0.0', port=4001)
        log.info('arrêt normal de l\'application')
    except Exception as ex:
        log.exception('l\'application s\'est arretée à cause d\'une erreur inattendue')
        pass
