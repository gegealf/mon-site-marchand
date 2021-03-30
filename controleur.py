from flask import render_template, session, request, redirect, url_for, abort

import logging
import hashlib
import re
from modele import MaBaseDeDonnees as MBDD

log = logging.getLogger(__name__)


def page_d_accueil():
    """                 """
    liste_categories = _recuperer_categories()
    liste_produits = _recuperer_liste_produits()
    session['page_precedente'] = []
    if not session.get('vous_etes_loggue'):
        log.debug('connexion à la page d\'accueil SANS authentification')
        return render_template("page_d_accueil.html", message="",
                               liste_categories=liste_categories, lenc=len(liste_categories),
                               liste_produits=liste_produits
                               )

    log.debug('connexion à la page d\'accueil AVEC authentification')
    message1 = "bienvenue"
    message2 = message1 + " " + session.get('utilisateur')
    liste_categories = _recuperer_categories()
    return render_template("page_d_accueil.html", message1=message1, message2=message2,
                           liste_categories=liste_categories, lenc=len(liste_categories),
                           liste_produits=liste_produits, nombre_produits_dans_panier=len(session.get('panier'))
                           )


def page_d_authentification():
    """          """
    log.debug('connexion à la page d\'authentification')
    message_d_erreur = None
    page_precedente = session.get('panier')
    pp = page_precedente
    pp.append(_redirect_url())
    session['page_precedente'] = pp
    if request.method == 'POST':
        mdp_utilisateur = request.form['mot_de_passe']
        email_utilisateur = request.form['email']
        compte_utilisateur_valide = _verifier_le_compte(email_utilisateur, mdp_utilisateur)
        if compte_utilisateur_valide != "vrai":
            session['vous_etes_loggue'] = False
            if compte_utilisateur_valide == "accès_admin":
                session['vous_etes_loggue'] = 'jesuisadminpastoi'
                return redirect(url_for('page_administrateur'))
            log.debug('erreur lors de l\'authentification')
            message_d_erreur = 'erreur lors de l\'authentification, veuillez recommencer'
        else:
            log.debug('connexion à la page d\'accueil/fiche_produit après authentification')
            session['vous_etes_loggue'] = True
            session['panier'] = []
            return redirect(session.get('page_precedente')[0])

    return render_template('page_d_authentification.html', message_d_erreur=message_d_erreur)


def deconnexion():
    """                 """
    log.debug('deconnexion du compte effectuée et panier vidé')
    session['vous_etes_loggue'] = False
    session['panier'] = []
    return redirect(_redirect_url())


def page_administrateur():
    """                  """
    if session.get('vous_etes_loggue') != 'jesuisadminpastoi':
        log.error('tentative de connexion à la page administrateur sans autorisation')
        return render_template('page_d_erreur.html')
    log.debug('connexion à la page administrateur')
    message = "bienvenue"
    return render_template('page_administrateur.html', message=message)


def page_creation_compte_utilisateur():
    """                                     """
    log.debug('connexion à la page de création de compte utilisateur')
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
        if _verifier_format_email(email_utilisateur) and _verifier_format_mdp(mdp_utilisateur) and \
                _verifier_format_donnees(utilisateur):
            log.debug('formats de l\'adresse mail, du mot de passe et des données valides')
            db = MBDD()
            if not db.verifier_email(email_utilisateur):
                log.debug('ajout du compte utilisateur à la base de données')
                db = MBDD()
                db.ajouter_utilisateur(utilisateur)
                message = "votre compte à bien été enregistré: "
                return render_template('page_creation_compte_utilisateur.html', message=message)
            log.debug('erreur lors de la validation del\'email: déjà utilisé')

        message_d_erreur = "erreur lors de la validation, veuillez recommencer"
        return render_template('page_creation_compte_utilisateur.html', message_d_erreur=message_d_erreur)

    return render_template('page_creation_compte_utilisateur.html')


def page_fiche_produit(numero_produit):
    """                   """
    session['page_precedente'] = []
    db = MBDD()
    if not db.verifier_numero_produit(numero_produit):
        log.error('tentative de connexion à une fiche produit inexistante')
        return render_template('page_d_erreur.html')

    produit = db.recuperer_produit(numero_produit)
    infos_produit = produit[4].split('_', 2)
    infos = [
        infos_produit[2].split('.', 1)[0].replace('_', ' '),
        infos_produit[0].split('/', 1)[1],
        infos_produit[1]
    ]
    if not session.get('vous_etes_loggue'):
        log.debug('connexion SANS authentification à la fiche du produit avec le numero: %s', numero_produit)
        return render_template('page_fiche_produit.html', numero_produit=numero_produit, produit=produit,
                               message="", infos=infos
                               )

    log.debug('connexion AVEC authentification à la fiche du produit avec le numero: %s', numero_produit)
    message1 = "bienvenue"
    message2 = message1 + " " + session.get('utilisateur')
    return render_template('page_fiche_produit.html', numero_produit=numero_produit, produit=produit,
                           message1=message1, message2=message2, infos=infos,
                           nombre_produits_dans_panier=len(session.get('panier'))
                           )


def page_panier():
    """                 """
    if not session.get('vous_etes_loggue'):
        log.error('tentative de connexion SANS authentification à la page panier')
        return render_template('page_d_erreur.html')
    db = MBDD()
    liste_produits = {}
    for numero_produit in session.get('panier'):
        # TODO: prévoir cas plusieurs fois le même produit
        liste_produits[numero_produit] = db.recuperer_produit(numero_produit)

    log.debug('accès à la page panier avec les produit numero: %s dans le panier', session['panier'])
    message1 = "bienvenue"
    message2 = message1 + " " + session.get('utilisateur')
    message3 = "panier"
    return render_template('page_panier.html', liste_produits=liste_produits, message1=message1, message2=message2,
                           message3=message3
                           )


def ajouter_au_panier(numero_produit):
    """                 """
    if not session.get('vous_etes_loggue'):
        return redirect(_redirect_url())

    log.debug('ajout du produit numero: %s dans le panier', numero_produit)
    session['panier'] += [numero_produit]
    return redirect(_redirect_url())


def supprimer_du_panier(numero_produit):
    """                 """
    if not session.get('vous_etes_loggue'):
        return render_template('page_d_erreur.html')
    log.debug('suppression du produit numero: %s dans le panier', numero_produit)
    ma_nouvelle_liste = session.get('panier')
    ma_nouvelle_liste.remove(numero_produit)
    session['panier'] = ma_nouvelle_liste
    if len(session.get('panier')) == 0:
        return redirect(url_for('page_d_accueil'))

    return redirect(_redirect_url())


def page_d_erreur():
    return render_template('page_d_erreur.html')


def test_500_html():
    """             """
    render_template('page_qui_n_existe_pas.html')


def test_500_serveur():
    """             """
    db = MBDD()
    r = db.mauvaise_requete()
    return r


def __hashage_mdp__(mot_de_passe_en_clair):
    """ création d'un mot de passe hashé """
    log.debug('hashage du mot de passe')
    a = bytes(mot_de_passe_en_clair, "utf-8")
    mdp_hashe = hashlib.sha256(a).hexdigest()
    return mdp_hashe


def _verifier_le_compte(email_utilisateur, mdp_utilisateur):
    """ appel des méthodes de classe MaBaseDeDonnees permettant de vérifier le compte avec email/mot de passe """
    log.debug('verification email et mot de passe')
    db = MBDD()
    mdp_hashe = __hashage_mdp__(mdp_utilisateur)
    access1 = db.verifier_si_compte_utilisateur_existe_deja(email_utilisateur, mdp_hashe)
    if access1 == "vrai":
        session['utilisateur'] = db.trouver_nom_prenom_utilisateur(email_utilisateur, mdp_hashe)
        return "vrai"
    else:
        access2 = db.verifier_si_compte_administrateur_existe_deja(email_utilisateur, mdp_hashe)
        if access2 == "vrai":
            return "accès_admin"

    return "faux"


def _verifier_format_email(email_utilisateur):
    """                                     """
    log.debug('vérification du format de l\'adresse mail')
    if (re.search("^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$", email_utilisateur)):
        return True

    log.debug('erreur de format de l\'adresse mail')
    return False


def _verifier_format_mdp(mdp_utilisateur):
    log.debug('vérification du format du mdp')
    if (
            re.search("^(?=.*?[A-Z])(?=(.*[a-z]){1,})(?=(.*[\d]){1,})(?=(.*[\W]){1,})(?!.*\s).{8,14}$",
                      mdp_utilisateur)):
        return True

    log.debug('erreur de format du mdp')
    return False


def _verifier_format_donnees(utilisateur):
    """                                     """
    log.debug('vérification du format des données')
    if utilisateur[2] and utilisateur[3] and utilisateur[4] and utilisateur[4].isdigit() \
            and (len(utilisateur[4]) == 10 or len(utilisateur[4]) == 13) \
            and utilisateur[6] and utilisateur[7] and utilisateur[8]:
        return True

    log.debug('erreur au niveau des données utilisateurs')
    return False


def _recuperer_categories():
    """ ici on peut définir pour l'ensemble de l'application, les onglets et
    leur ordre d'apparition dans la page d'accueil """
    liste_categories = ['Nouveautés et baisses de prix', 'Cartes mémoire', 'Clés USB', 'SSD', 'HDD', 'RAM']
    return liste_categories


def _recuperer_liste_produits():
    """ fournie tous les produits de la table sous la forme d'un dictionnaire,
        avec en clé la catégorie et en valeur la liste des produits de cette catégorie,
        pour permettre l'affichage par onglets catégories dans la page d'accueil
    """
    db = MBDD()
    liste_categories = _recuperer_categories()
    return db.recuperer_liste_produits(liste_categories)


def _redirect_url():
    return request.args.get('next') or request.referrer or url_for('page_d_accueil')
