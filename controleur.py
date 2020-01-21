from flask import render_template, session, request, flash, redirect, url_for
import logging
import hashlib
from modele import MaBaseDeDonnees as MBDD

log = logging.getLogger(__name__)


def page_d_accueil():
    if not session.get('vous_etes_loggue'):
        log.debug('connexion à la page d\'accueil sans authentification')
        return render_template("page_d_accueil.html", message="")  # lien vers la page d'accueil

    log.debug('connexion à la page d\'accueil avec authentification')
    message1 = "bienvenue"
    message2 = message1 + " " + session.get('utilisateur')
    return render_template("page_d_accueil.html", message1=message1, message2=message2)  # lien vers la page d'accueil


def page_d_authentification():
    log.debug('connexion à la page d\'authentification')
    message_d_erreur = None
    if request.method == 'POST':
        log.debug('tentative d\'authentification')
        mdp_utilisateur = request.form['mot_de_passe']
        email_utilisateur = request.form['email']
        compte_utilisateur_valide = verifier_le_compte(email_utilisateur, mdp_utilisateur)
        if compte_utilisateur_valide != "vrai":
            if compte_utilisateur_valide == "accès_admin":
                return redirect(url_for('page_administrateur'))

            log.debug('erreur lors de l\'authentification')
            session['vous_etes_loggue'] = False
            message_d_erreur = 'erreur lors de l\'authentification, veuillez recommencer'

        else:
            log.debug('connexion à la page d\'accueil après authentification')
            session['vous_etes_loggue'] = True

            return redirect(url_for('page_d_accueil'))

    return render_template('page_d_authentification.html', message_d_erreur=message_d_erreur)


def deconnexion():
    log.debug('deconnexion du compte')
    session['vous_etes_loggue'] = False
    return render_template("page_d_accueil.html")


def page_administrateur():
    log.debug('connexion à la page administrateur')
    session['vous_etes_loggue'] = False
    message = "bienvenue"
    return render_template('page_administrateur.html', message=message)


def __hashage_mdp__(mot_de_passe_en_clair):
    """ création d'un mot de passe hashé """
    log.debug('hashage du mot de passe')
    a = bytes(mot_de_passe_en_clair, "utf-8")
    mdp_hashe = hashlib.sha256(a).hexdigest()
    return mdp_hashe


def verifier_le_compte(email_utilisateur, mdp_utilisateur):
    """ appel des méthodes de classe MaBaseDeDonnees permettant de vérifier le compte avec email/mot de passe """
    log.debug('verification email/mot de passe')
    mdp_hashe = __hashage_mdp__(mdp_utilisateur)
    db = MBDD()  # création d'une instance de ma base de données
    access1 = db.verifier_si_compte_utilisateur_existe_deja(email_utilisateur, mdp_hashe)
    if access1 == "vrai":
        session['utilisateur'] = db.trouver_nom_prenom_utilisateur(email_utilisateur, mdp_hashe)
        return "vrai"
    else:
        access2 = db.verifier_si_compte_administrateur_existe_deja(email_utilisateur, mdp_hashe)
        if access2 == "vrai":
            return "accès_admin"

    return "faux"


def page_creation_compte_utilisateur():
    log.debug('connexion à la page de création de compte utilisateur')
    message_d_erreur = ""
    if request.method == 'POST':
        email_utilisateur = request.form['email']
        db = MBDD()
        if not db.verifier_email(email_utilisateur):
            mdp_utilisateur = request.form['mot_de_passe']
            nom_utilisateur = request.form['nom']
            prenom_utilisateur = request.form['prenom']
            date_de_naissance_utilisateur = request.form['date_de_naissance']
            numero_de_telephone_utilisateur = request.form['numero_de_telephone']
            numero_de_voie = request.form['numero_de_voie']
            nom_de_voie = request.form['nom_de_voie']
            code_postal = request.form['code_postal']
            ville = request.form['ville']
            mdp_hashe = __hashage_mdp__(mdp_utilisateur)
            utilisateur = [
                email_utilisateur,
                mdp_hashe,
                nom_utilisateur,
                prenom_utilisateur,
                date_de_naissance_utilisateur,
                numero_de_telephone_utilisateur,
                numero_de_voie,
                nom_de_voie,
                code_postal,
                ville
            ]
            db.ajouter_utilisateur(utilisateur)
            message = "votre compte à bien été enregitré"
            return render_template('page_creation_compte_utilisateur.html', message=message)

        message_d_erreur = "erreur lors de l'authentification, veuillez recommencer"
        return render_template('page_creation_compte_utilisateur.html', message_d_erreur=message_d_erreur)

    return render_template('page_creation_compte_utilisateur.html')