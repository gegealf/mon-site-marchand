from flask import render_template, session
import logging
from modele import MaBaseDeDonnees as MBDD

log = logging.getLogger(__name__)


def page_d_accueil():
    if not session.get('vous_etes_loggue'):
        pass
    else:
        pass
    log.debug('connexion à la page d\'accueil')
    return render_template("page_d_accueil.html")  # lien vers la page d'accueil


def authentification():
    if not session.get('vous_etes_loggue'):
        return render_template("page_d_accueil.html")
    log.debug('connexion à la page d\'authentification')
    return render_template("page_d_authentification.html")
