# coding: utf8
# JD Metro_CMS (nom provisoir) en attente d'une meilleur idée

import os
import time
import uuid
import hashlib
import requests
from courriel import *
from validation import *

from ua_parser import user_agent_parser
from werkzeug.utils import secure_filename
 
from datetime import datetime
from flask import g
from flask import json
from flask import Flask
from flask import session
from flask import jsonify
from flask import url_for
from flask import request
from flask import Response
from flask import make_response
from flask import redirect
from functools import wraps
from database import Articles
from database import Database
from flask import render_template


from flask_wtf import Form
from wtforms import TextAreaField, SubmitField, StringField
from werkzeug.utils import secure_filename


app = Flask(__name__, static_url_path="", static_folder="static")
UPLOAD_FOLDER = 'static/images'
DELETE_FOLDER = 'images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DELETE_FOLDER'] = DELETE_FOLDER

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database

def authentication_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not is_authenticated(session):
            return render_template('error_html.html', error_html="401",
                                   error_message=u"Non autorisé"), 401
        return f(*args, **kwargs)
    return decorated

def admin(f):
    @wraps(f)
    def decorated2(*args, **kwargs):
        if 2 < getRight():
            return render_template('error_html.html', error_html="401",error_message=u"Non autorisé"), 401
        return f(*args, **kwargs)
    return decorated2

def writer(f):
    @wraps(f)
    def decorated3(*args, **kwargs):
        if 3 < getRight():
            return render_template('error_html.html', error_html="401",error_message=u"Non autorisé"), 401
        return f(*args, **kwargs)
    return decorated3


def is_authenticated(session):
    return "id" in session

@app.route('/')
def start_page():
    Log('star_page')
    articles=get_db().select_liste()
    if verifierLangue() == 'FR':
        return render_template('temp_intro_articles.html',articles=articles,title=u'Dernières Nouvelles')
    else:
        return render_template('temp_intro_articles.html',articles=articles,title='Lates News', langue=1)

@app.route('/login', methods=['POST','GET'])
def login_page():
    return render_template('login.html')

@app.route('/login/change/password', methods=['POST','GET'])
def login_page_change_password():
    return render_template('new_password.html')

@app.route('/login/demande/motpasse', methods=['POST'])
def demande_recuperation_motpasse():
    data = u"La demande de récupération a été envoyée"
    courriel = request.form['courriel']
    token = uuid.uuid4().hex
    if not get_db().valider_courriel(courriel):
        get_db().save_recuperation(courriel, token)
        message_courriel(courriel, token, render_template(
                         'courriel_motpasse.html', token=token, site=os.environ.get('site')),
                         "Recuperation")
        return render_template('new_password.html',
                               data=data)
    else:
        return render_template('new_password.html',
                               data=u"Le courriel n'existe pas")
@app.route('/logout')
@authentication_required
def logout():
    if "id" in session:
        id_session = session["id"]
        session.pop('id', None)
        get_db().delete_session(id_session)
        Log('LOGOUT')
    return redirect("/")


@app.route('/affichage_login', methods=["GET"])
def affichage_login():
    if "id" in session:
        return render_template('logout_tab.html')
    else:
        return render_template('login_tab.html')

@app.route('/motpasseperdue/<id_token>')
def motpasseperdue(id_token):
    data = u'Le délais de renouvellement du mot de passe a été dépassé'
    if "id" in session:
        print 'test1'
        return render_template('error_html.html', error_html="401",
                               error_message=u"Non autorisé"), 401
    trenteminute = 1800
    res = get_db().recuperer_motpasse(id_token)
    print "mot passe perdue temp"
    print res
    print time.mktime(datetime.now().timetuple())
    if res is None:
        print 'test2'
        return redirect(url_for('page_not_found401')), 401
    if ((time.mktime(datetime.now().timetuple()))-res) > trenteminute:
        return render_template('new_password.html',
                               data=data)
    else:
        return render_template('temp_changement_mot_passe.html', token=id_token)

@app.route('/changer_mot_passe', methods=['POST'])
def changer_mot_passe():
    motpasse = request.form["motpasse"]
    motpasse2 = request.form["motpasse2"]
    token = request.form["token"]
    courriel = get_db().courriel_recuperation(token)
    if courriel is False and get_db().valider_courriel(courriel):
        return render_template('temp_changement_mot_passe.html',
                               data=u"Problème à l'identification")
    erreurs = valider_mot_passe(motpasse, motpasse2)
    if any(erreurs):
        return render_template('temp_changement_mot_passe.html',
                               erreurs=erreurs, token=token)
    else:
        salt = uuid.uuid4().hex
        hash = hashlib.sha512(motpasse + salt).hexdigest()
        get_db().update_mot_passe(courriel, salt, hash)
        get_db().delete_recuperation(token)
        return render_template('temp_changement_mot_passe.html',
                               data=u"Mot de passe changé")

@app.route('/login/validation', methods=['POST','GET'])
def login_validation():
    courriel = request.form['username']
    password = request.form['password']
    hash = get_db().get_user_login_info(courriel)
    if courriel == "correcteur" and password == "secret":
        id_session = uuid.uuid4().hex
        get_db().save_session(id_session, courriel)
        session["id"] = id_session
        Log('acces grant')
        return redirect("/")
    print hash
    if hash == None or hash[0] == None:
        Log('wrong password')
        return render_template('login.html',error='wrong user/password')
    print 'passe la'
    salt = hash[0]
    hashed_password = hashlib.sha512(password + salt).hexdigest()
    if hashed_password == hash[1]:
        # Accès autorisé
        id_session = uuid.uuid4().hex
        get_db().save_session(id_session, courriel)
        session["id"] = id_session
        Log('acces grant')
        return redirect("/")
    else:
        Log('wrong password')
        return render_template('login.html',error='wrong user/password')


@app.route('/gestion/invitation')
@authentication_required
def inviter_collaborateur():
    roles = get_db().get_roles()
    print roles
    return render_template('temp_invitation.html',roles=roles)

@app.route('/gestion/invitation/<token>')
def nouveau_usager(token):
    if "id" in session:
        return render_template('error_html.html', error_html="401",
                               error_message=u"Non autorisé"), 401
    res = get_db().valider_invitation(token)
    if res != None:
        print res
        return render_template('temp_create_new_user.html', token=token)
    else:
        return render_template('error_html.html', error_html="401",
                               error_message=u"Non autorisée"), 401

@app.route('/gestion/send/invitation', methods=["POST"])
@authentication_required
def envoyer_invitation():
    courriel = request.form['courriel']
    role = request.form['role']
    token = uuid.uuid4().hex
    if get_db().valider_courriel(courriel) is False:
        data = u"Il y a déja un compte associé à ce courriel"
        return render_template('temp_invitation.html',
                               data=data)
    if get_db().inviter_courriel(courriel) is True:
        get_db().save_invitation(courriel, token, role)
        message_courriel(courriel, token, render_template(
                         'courriel_invitation.html', token=token),
                         "invitation")
        return render_template('temp_invitation.html',
                               data=u"Invitation envoyées")
    elif get_db().inviter_courriel(courriel) is False:
        token = get_db().token_invitation(courriel)
        message_courriel(courriel, token, render_template(
                         'courriel_invitation.html', token=token),
                         "invitation rappel")
        return render_template('temp_invitation.html',
                               data=u"Invitation envoyées à nouveau")
    else:
        return render_template('temp_invitation.html',
                               data=u"Le courriel existe déjà")

@app.route('/gestion/user/update', methods=['POST','GET'])
@authentication_required
def update_user_test():
    if request.method =="POST":
        user = request.json
        get_db().update_user(user['id'],"",user['nom'],user['courriel'],user['role'], user['picture'],user['actif'])
        roles = get_db().get_roles()
        print user
    return render_template('usager.html',user=user,roles=roles, role=int(user['role']) )

@app.route('/gestion/user/list', methods=["POST","GET"])
@authentication_required
@admin
def list_user():
    users = get_db().list_all_user()
    roles = get_db().get_roles()
    return render_template('temp_manage_user.html', users=users, roles=roles)

@app.route('/gestion/user/profil', methods=["POST","GET"])
@authentication_required
def user_profil():
    return render_template('temp_profil_user.html')

@app.route('/gestion/usager/update/<id_user>', methods=["POST","GET"])
@authentication_required
@admin
def update_user(id_user):
    users = get_db().list_all_user()
    roles = get_db().get_roles()
    print roles
    return render_template('temp_manage_user.html', users=users, roles=roles)

@app.route('/gestion/create/user', methods=["POST"])
@authentication_required
def invitation():
    nom = request.form["nom"]
    courriel = request.form["courriel"]
    motpasse = request.form["motpasse"]
    motpasse2 = request.form["motpasse2"]
    token = request.form["token"]
    erreur_data = valider_donnees_usager(nom, courriel, motpasse, motpasse2)
    erreurs = valider_mot_passe(motpasse, motpasse2)
    if any(erreurs) or any(erreur_data):
        return render_template('temp_create_new_user.html',
                               erreurs=erreurs, token=token, name=nom,
                               erreur_data=erreur_data, courriel=courriel)
    salt = uuid.uuid4().hex
    hash = hashlib.sha512(motpasse + salt).hexdigest()
    get_db().ajout_utilisateur(nom, courriel, salt, hash)
    get_db().delete_invitation(token)
    return render_template('login.html',
                           message=u'Votre code usager a été créer')

@app.route('/liste')
def intro():
    articles=get_db().select_liste()
    if verifierLangue() == 'FR':
        return render_template('temp_intro_articles.html',articles=articles,title=u'Dernières Nouvelles')
    else:
        return render_template('temp_intro_articles.html',articles=articles,title='Lates News', langue=1)

@app.route('/gestion/creer/article')
def create_article():
    photos = get_db().liste_medias()
    categories = get_db().liste_categories()
    return render_template('temp_creat_article.html', photos=photos,categories=categories)

@app.route('/gestion/create/user')
@authentication_required
@admin
def create_user():
    print controlRight(2)
    print 'passe la'
    return render_template('temp_create_new_user.html')


@app.route('/save/nouveau', methods=['POST','GET'])
@authentication_required
@writer
def nouveau():
    url = request.form['URL']
    datepub = request.form['datepublication']
    tag = request.form['tag']
    etiquettes = request.form['etiquettes']
    categorie = request.form['categorie']
    titre_fr = request.form['titre_fr']
    titre_ang = request.form['titre_ang']
    auteur = request.form['auteur']
    photo = request.form['photo']
    texte_fr = request.form['editor_fr']
    texte_ang = request.form['editor_ang']
    gallery = request.form['gallery_html']
    comments_on = request.form.get('comments_on')
    print comments_on
    if comments_on != 'true':
        comments_on = 'false'
    article = Articles("", url, auteur, datepub, titre_fr, titre_ang, texte_fr, texte_ang, categorie,
                           etiquettes, tag, photo, "", "", gallery, comments_on)
    print article
    erreur_data = valider_acticle(article)
    if any(erreur_data):
        photos = get_db().liste_medias()
        categories = get_db().liste_categories()
        return render_template('temp_creat_article.html', articles=article,
                               erreur_data=erreur_data, photos=photos,categories=categories)
    else:
        photos = get_db().liste_medias()
        categories = get_db().liste_categories()
        get_db().insert_article(url,auteur,datepub,titre_fr,titre_ang,texte_fr,texte_ang,categorie,etiquettes,tag,photo,gallery,comments_on)
    return render_template('temp_creat_article.html', photos=photos,categories=categories)

@app.route('/save/miseajour/<id_article>', methods=['POST','GET'])
@authentication_required
@writer
def afficher_update(id_article):
    article = get_db().get_info_article(id_article)
    erreur_data = valider_acticle(article)
    photos = get_db().liste_medias()
    categories = get_db().liste_categories()
    return render_template('temp_creat_article.html', articles=article,
                               erreur_data=erreur_data, photos=photos, update='update',categories=categories)

@app.route('/save/miseajour', methods=['POST','GET'])
@authentication_required
@writer
def save_update():
    unique = request.form['id']
    url = request.form['URL']
    datepub = request.form['datepublication']
    tag = request.form['tag']
    etiquettes = request.form['etiquettes']
    categorie = request.form['categorie']
    titre_fr = request.form['titre_fr']
    titre_ang = request.form['titre_ang']
    auteur = request.form['auteur']
    photo = request.form['photo']
    texte_fr = request.form['editor_fr']
    texte_ang = request.form['editor_ang']
    gallery = request.form['gallery_html']
    comments_on = request.form.get('comments_on')
    if comments_on != 'true':
        comments_on = 'false'
    article = Articles(unique,url,auteur,datepub,titre_fr,titre_ang,texte_fr,texte_ang,categorie,etiquettes,tag,photo,"","",gallery,comments_on)
    erreur_data = valider_acticle(article)
    if any(erreur_data):
        photos = get_db().liste_medias()
        categories = get_db().liste_categories()
        return render_template('temp_creat_article.html', articles=article,
                               erreur_data=erreur_data, photos=photos, update='update',categories=categories)
    else:
        get_db().update_article(unique,url,auteur,datepub,titre_fr,titre_ang,texte_fr,texte_ang,categorie,etiquettes,tag,photo,gallery,comments_on)
    return redirect(url_for('loadupdate'))

@app.route('/gestion/liste/articles', methods=['POST','GET'])
@authentication_required
@writer
def loadupdate():
    articles = get_db().all_liste()
    return render_template('temp_listes_articles.html',articles=articles)

@app.route('/save/fichiers', methods=['POST','GET'])
@authentication_required
@writer
def upload():
    info_upload = {}
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file[]' not in request.files:
            return redirect(request.url)
        uploaded_files = request.files.getlist("file[]")
        for tempfile in uploaded_files:
            file = tempfile.filename
            if file == '':
                return redirect(request.url)
            if allowed_file(file):
                if get_db().valider_medias(secure_filename(file)):
                    filename = secure_filename(file)
                    tempfile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    get_db().save_medias('admin', filename)
                else:
                    print 'La photo existe'
            else:
                print 'fichier interdit'
    photos = get_db().liste_medias()
    if verifierLangue() == 'FR':
        return render_template('temp_upload.html',photos=photos)
    else:
        return render_template('temp_upload.html',photos=photos,langue=1)

@app.route('/delete/<filename>', methods=['POST','GET'])
@authentication_required
@admin
def delete_media(filename):
    if filename <> None and get_db().valider_medias(filename) == False:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        get_db().delete_medias(filename)
        photos = get_db().liste_medias()
        return redirect(url_for('upload'))
    else:
        photos = get_db().liste_medias()
        return redirect(url_for('upload'))

@app.route('/delete/article/<id_article>', methods=['POST','GET'])
@authentication_required
@admin
def delete_article(id_article):
    get_db().delete_article(id_article)
    return redirect(url_for('loadupdate'))

@app.route('/article/<categorie>/<url_article>', methods=['POST','GET'])
def afficher_article(categorie,url_article):
    article=get_db().get_url_article(url_article)
    comments=get_db().get_comments(article.unique)
    print 
    Log('article: '+article.titre_fr)
    if verifierLangue() == 'FR':
        return render_template('temp_article.html',articles=article,title=u'Catégorie : '+categorie,comments=comments)
    else:
        return render_template('temp_article.html',articles=article,title='Category : '+categorie, langue=1,comments=comments)

@app.route('/categorie/<id_categorie>', methods=['POST','GET'])
def afficher_article_categorie(id_categorie):
    Log('afficher categories: '+id_categorie)
    articles=get_db().get_categorie_article(id_categorie)
    if verifierLangue() == 'FR':
        return render_template('temp_intro_articles.html',articles=articles,title=id_categorie)
    else:
        return render_template('temp_intro_articles.html',articles=articles,title=id_categorie, langue=1)

@app.route('/auteur/<id_auteur>', methods=['POST','GET'])
def afficher_article_auteur(id_auteur):
    articles=get_db().get_categorie_article(id_auteur)
    if verifierLangue() == 'FR':
        return render_template('temp_intro_articles.html',articles=articles,title=u'Catégorie : '+id_auteur)
    else:
        return render_template('temp_intro_articles.html',articles=articles,title='Category : '+id_auteur, langue=1)

@app.route('/menu_cat', methods=['POST','GET'])
def menu_categories():
    menu_cat = get_db().liste_categories()
    if verifierLangue() == 'FR':
        return render_template('menu_categories.html',menu_cat=menu_cat)
    else:
        return render_template('menu_categories.html',menu_cat=menu_cat,langue=1)

@app.route('/comments', methods=['POST','GET'])
def comments():
    if request.method =="POST":
        content = request.json
        get_db().save_comments(getUser(),content['id_article'],content['comment'])
        comments=get_db().get_comments(content['id_article'])
    return render_template('comments.html',comments=comments)

@app.route('/gestion/comments', methods=['POST','GET'])
@authentication_required
def validate_comments():
	mycomments()
	comments=get_db().get_comments_unvalidated()
	return render_template('temps_admin_comment.html',comments=comments)

@app.route('/valider/comments/<id_comments>', methods=['POST','GET'])
@authentication_required
@writer
def check_comments(id_comments):
    get_db().comments_validated(id_comments)
    return '',200

@app.route('/unvalider/comments/<id_comments>', methods=['POST','GET'])
@authentication_required
@writer
def uncheck_comments(id_comments):
    get_db().comments_unvalidated(id_comments)
    return '',200

@app.route('/valider/signaler/comments/<id_comments>', methods=['POST','GET'])
@authentication_required
@writer
def signal_comments(id_comments):
    get_db().comments_validated_signaled(id_comments)
    return '',200

@app.route('/validated/comments', methods=['POST','GET'])
@authentication_required
def validated_comments():
    comments = get_db().get_valid_comments()
    return render_template('liste_comments.html',comments=comments)

@app.route('/unvalidated/comments', methods=['POST','GET'])
@authentication_required
def unvalidated_comments():
    comments = get_db().get_comments_unvalidated()
    return render_template('liste_comments.html',comments=comments)

@app.route('/signaled/comments', methods=['POST','GET'])
@authentication_required
@writer
def singaled_comments():
    comments = get_db().get_signaled_comments()
    return render_template('liste_comments.html',comments=comments)

@app.route('/all/comments', methods=['POST','GET'])
@authentication_required
@writer
def all_comments():
    comments = get_db().get_all_comments()
    return render_template('liste_comments.html',comments=comments)

@app.route('/recherche', methods=['POST','GET'])
def search_term():
    rechercher='vide'
    resp=''
    if request.method =='POST':
        rechercher = request.form['recherche']
    else:
        rechercher = request.cookies.get('recherche')
    articles = get_db().select_recherche(rechercher)
    if verifierLangue() == 'FR':
        resp = make_response(render_template('temp_intro_articles.html',articles=articles,title=u'Resultats de recherche',recherche=rechercher))
    else:
        resp = make_response(render_template('temp_intro_articles.html',articles=articles,title='Search Result', langue=1,recherche=rechercher))
    resp.set_cookie('recherche', rechercher)
    Log('search: '+rechercher)
    return resp

@app.route('/gestion', methods=['POST','GET'])
@authentication_required
def gestion_admin():
    return render_template('temp_menu_admin.html')

def validerSession(message):
    data = message
    if "id" in session:
        return render_template('error_html.html', error_html="401",
                               error_message=u"Non autorisé"), 401
    else:
        return True

@app.route('/sidepanel/<type>', methods=['POST','GET'])
def sidepanel(type):
    if request.method == "GET":
        return 0
    else:
        return 0
        
app.secret_key = "77458cd6536d0f464cd218d9f6b20d78"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def valider_acticle(articles):
    erreur_data = {}
    if valider_champs(articles.auteur):
        erreur_data.update({"auteur": "Nom d'auteur invalide"})
    if valider_champs(articles.titre_fr):
        erreur_data.update({"titre_fr": "Titre invalide"})
    if valider_champs(articles.titre_ang):
        erreur_data.update({"titre_ang": "Titre invalide"})
    if valider_texte(articles.texte_fr):
        erreur_data.update({"texte_fr": "Paragraphe est invalide"})
    if valider_texte(articles.texte_ang):
    	erreur_data.update({"texte_ang": "Paragraphe est invalide"})
    if valider_mydate(articles.datepub):
        valider_mydate(articles.datepub)
        erreur_data.update({"datepub": "Date est invalide"})
    if articles.unique == 0:
        if valider_url(articles.url):
            erreur_data.update({"URL": "l'url est invalide ou il exite deja"})
    else:
        if valider_url_2(articles.url,articles.unique):
            erreur_data.update({"URL": "l'url est invalide ou il exite deja"})
    return erreur_data

def valider_mydate(mydate):
    if not mydate:
        return True
    return False

def valider_texte(texte):
    if not texte:
        return True

def valider_url(url):
    if not url:
        return True
    for lettre in url:
        if not(lettre == "-" or lettre.isalnum()):
            return True
    return get_db().select_url(url)

def valider_url_2(url,unique):
    if not url:
        return True
    for lettre in url:
        if not(lettre == "-" or lettre.isalnum()):
            return True
    return get_db().valider_url_2(url,unique)

def enlever_accent(texte):
    return unicodedata.normalized('NFKD', texte).encode('ASCII', 'ignore')  

def valider_champs(champs):
    if not champs:
        return True
    for lettre in champs:
        if not (lettre.isalnum() or lettre == " "):
            return True
    return False

def verifierLangue():
    langue = request.cookies.get('langue')
    if langue == None:
        return 'FR'
    else:
        return langue

def getUser():
    if "id" in session:
        id_session = session["id"]
        user_name = get_db().get_User_Session(id_session)
    else:
        user_name = "invited"
    return user_name

def getRight():
    if "id" in session:
        id_session = session["id"]
        user_name = get_db().get_User_Right(id_session)
    else:
        user_name = "invited"
    return user_name

def controlRight(level):
    print level < getRight()
    if level < getRight():
        print 'passe ici'
        return render_template('error_html.html', error_html="401",error_message=u"Non autorisé"), 401


def Log(action):
    id_user=getUser()
    get_db().log_activity(id_user,action, request.user_agent.platform, request.user_agent.browser+" "+request.user_agent.version, request.environ['REMOTE_ADDR'])

def kept_search():
    search = request.cookies.get('recherche')
    return search
    
def mycomments():
	user = getUser()
	print user

@app.errorhandler(400)
def page_not_found400(e):
    return render_template('error_html.html', error_html="400",
                           error_message=u"Requête erronée"), 400

@app.errorhandler(401)
def page_not_found401(e):
    return render_template('error_html.html', error_html="401",
                           error_message=u"Non autorisé"), 401

@app.errorhandler(404)
def page_not_found404(e):
    return render_template('error_html.html', error_html="404",
                           error_message="Page introuvable"), 404

@app.errorhandler(405)
def page_not_found405(e):
    return render_template('error_html.html', error_html="405",
                           error_message=u"Méthode requête non autorisée"), 405

@app.errorhandler(500)
def page_not_found500(e):
    return render_template('error_html.html', error_html="500",
                           error_message="erreur serveur"), 500
