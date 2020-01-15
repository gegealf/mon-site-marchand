from flask import render_template
import logging

log = logging.getLogger(__name__)


def page_d_accueil():
    log.debug('connexion à la page d\'accueil')
    return render_template("page_d_accueil.html")  # lien vers la page d'accueil


def authentification():
    log.debug('connexion à la page d\'authentification')
    return render_template("page_d_authentification.html")
