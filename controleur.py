from flask import render_template, session, request, flash, redirect, url_for
import logging
import hashlib
from modele import MaBaseDeDonnees as MBDD
import re

log = logging.getLogger(__name__)


def page_d_accueil():
    """                 """
    liste_categories = recuperer_categories()
    liste_produits = recuperer_liste_produits()

    if not session.get('vous_etes_loggue'):
        log.debug('connexion à la page d\'accueil sans authentification')
        return render_template("page_d_accueil.html", message="",
                               liste_categories=liste_categories, lenc=len(liste_categories),
                               liste_produits=liste_produits
                               )  # lien vers la page d'accueil

    log.debug('connexion à la page d\'accueil avec authentification')
    message1 = "bienvenue"
    message2 = message1 + " " + session.get('utilisateur')
    liste_categories = recuperer_categories()
    return render_template("page_d_accueil.html", message1=message1, message2=message2,
                           liste_categories=liste_categories, lenc=len(liste_categories),
                           liste_produits=liste_produits
                           )  # lien vers la page d'accueil


def page_d_authentification():
    """          """
    log.debug('connexion à la page d\'authentification')
    message_d_erreur = None
    if request.method == 'POST':
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
    """                 """
    log.debug('deconnexion du compte effectuée')
    session['vous_etes_loggue'] = False
    return redirect(url_for('page_d_accueil'))


def page_administrateur():
    """                  """
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
    log.debug('verification email et mot de passe')
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
    """                                     """
    log.debug('connexion à la page de création de compte utilisateur')
    message_d_erreur = ''
    if request.method == 'POST':
        email_utilisateur = request.form['email']
        mdp_utilisateur = request.form['mot_de_passe']
        nom_utilisateur = request.form['nom']
        prenom_utilisateur = request.form['prenom']
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
            numero_de_telephone_utilisateur,
            numero_de_voie,
            nom_de_voie,
            code_postal,
            ville
        ]
        if verifer_format_email(email_utilisateur) and verifer_format_mdp(mdp_utilisateur) and \
                verifer_format_donnees(utilisateur):
            db = MBDD()
            log.debug('formats de l\'adresse mail, du mot de passe et des données valides')
            if not db.verifier_email(email_utilisateur):
                log.debug('ajout du compte utilisateur à la base de données')
                db.ajouter_utilisateur(utilisateur)
                message = "votre compte à bien été enregistré: "
                return render_template('page_creation_compte_utilisateur.html', message=message)
            log.debug('erreur lors de la validation del\'email: déjà utilisé')

        message_d_erreur = "erreur lors de la validation, veuillez recommencer"
        return render_template('page_creation_compte_utilisateur.html', message_d_erreur=message_d_erreur)

    return render_template('page_creation_compte_utilisateur.html')


def verifer_format_email(email_utilisateur):
    """                                     """
    log.debug('vérification du format de l\'adresse mail')
    if (re.search("^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$", email_utilisateur)):
        return True

    log.debug('erreur de format de l\'adresse mail')
    return False


def verifer_format_mdp(mdp_utilisateur):
    log.debug('vérification du format du mdp')
    if (re.search("^(?=.*?[A-Z])(?=(.*[a-z]){1,})(?=(.*[\d]){1,})(?=(.*[\W]){1,})(?!.*\s).{8,14}$", mdp_utilisateur)):
        return True

    log.debug('erreur de format du mdp')
    return False


def verifer_format_donnees(utilisateur):
    """                                     """
    log.debug('vérification du format des données')
    if utilisateur[2] and utilisateur[3] and utilisateur[4] and utilisateur[4].isdigit() \
            and (len(utilisateur[4]) == 10 or len(utilisateur[4]) == 13) \
            and utilisateur[6] and utilisateur[7] and utilisateur[8]:
        return True

    log.debug('erreur au niveau des données utilisateurs')
    return False


def recuperer_categories():
    """ ici on peut définir pour l'ensemble de l'application, les onglets et
    leur ordre d'apparition dans la page d'accueil """
    liste_categories = ['Nouveautés et baisses de prix', 'Cartes mémoire', 'Clés USB', 'SSD', 'HDD', 'RAM']
    return liste_categories


def recuperer_liste_produits():
    """ fournie tous les produits de la table sous la forme d'un dictionnaire,
        avec en clé la catégorie et en valeur la liste des produits de cette catégorie,
        pour permettre l'affichage par onglets catégories dans la page d'accueil
    """
    liste_categories = recuperer_categories()
    db = MBDD()
    return db.recuperer_liste_produits(liste_categories)


def page_fiche_produit(numero_produit):
    """                   """
    log.debug('connexion à la fiche du produit avec numero: %s', numero_produit)
    return render_template('page_fiche_produit.html', numero_produit=numero_produit)
