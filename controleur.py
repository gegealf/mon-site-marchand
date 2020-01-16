from flask import render_template, session, request, flash, redirect, url_for
import logging
from modele import MaBaseDeDonnees as MBDD

log = logging.getLogger(__name__)


def page_d_accueil():
    if not session.get('vous_etes_loggue'):
        log.debug('connexion à la page d\'accueil sans authentification')
        return render_template("page_d_accueil.html", message="Cliquez pour vous authentifier")

    log.debug('connexion à la page d\'accueil avec authentification')
    return render_template("page_d_accueil.html", message="bienvenue .....")  # lien vers la page d'accueil


def page_d_authentification():
    log.debug('connexion à la page d\'authentification')
    message_d_erreur = None
    if request.method == 'POST':
        log.debug('tentative d\'authentification')
        if request.form['mot_de_passe'] != 'gege' or request.form['email'] != 'admin@admin.gege':
            log.debug('erreur lors de l\'authentification')
            session['vous_etes_loggue'] = False
            message_d_erreur = 'erreur lors de l\'authentification, veuillez recommencer'
        else:
            log.debug('connexion à la page d\'accueil après authentification')
            session['vous_etes_loggue'] = True
            return redirect(url_for('page_d_accueil'))

    return render_template('page_d_authentification.html', message=message_d_erreur)
