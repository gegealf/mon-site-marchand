from flask import render_template
import logging

log = logging.getLogger(__name__)


def page_d_accueil():
    log.debug('connection starts')
    return render_template("page_d_accueil.html")  # lien vers la page d'accueil
