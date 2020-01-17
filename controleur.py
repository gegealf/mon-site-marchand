from flask import render_template, session, request, flash, redirect, url_for
import logging
import hashlib
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
        mdp_utilisateur = request.form['mot_de_passe']
        email_utilisateur = request.form['email']
        compte_valide = verifier_le_compte(email_utilisateur, mdp_utilisateur)
        if not compte_valide:
            log.debug('erreur lors de l\'authentification')
            session['vous_etes_loggue'] = False
            message_d_erreur = 'erreur lors de l\'authentification, veuillez recommencer'
        else:
            log.debug('connexion à la page d\'accueil après authentification')
            session['vous_etes_loggue'] = True
            return redirect(url_for('page_d_accueil'))

    return render_template('page_d_authentification.html', message=message_d_erreur)


def verifier_le_compte(email_utilisateur, mdp_utilisateur):
    """ call hash function and class DbHandler method to verify account """
    log.debug('verification email/mot de passe')
    mdp_hashe = __hashage_mdp__(mdp_utilisateur)
    db = MBDD()  # création d'une instance de ma base de données
    access = db.verifier_si_compte_existe_deja(email_utilisateur, mdp_hashe)
    if access == "vrais":
        return True
    return False


def __hashage_mdp__(mot_de_passe_en_clair):
    """ création d(un mot de passe hashé """
    log.debug('hashage du mot de passe')
    a = bytes(mot_de_passe_en_clair, "utf-8")
    mdp_hashe = hashlib.sha256(a).hexdigest()
    return mdp_hashe
