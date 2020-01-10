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

if __name__ == "__main__":  # python main.py
    import controleur

    app.add_url_rule('/', 'page_d_accueil', view_func=controleur.page_d_accueil)
    try:
        log.info('Application starting')
        app.run(host='127.0.0.1', port=8000)  # lancement de l'application en local
        # app.run(host='0.0.0.0', port=4001)
        log.info('Application end without exception')
    except Exception as ex:
        log.exception('Application end because of uncatching exception')
        pass
