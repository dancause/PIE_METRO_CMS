# coding: utf8
# JD Metro_CMS (nom provisoir) en attente d'une meilleur idée

import os
import time
import uuid
import hashlib
import requests

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

@app.route('/')
def start_page():
    Log('log')
    articles=get_db().select_liste()
    if verifierLangue() == 'FR':
        return render_template('temp_intro_articles.html',articles=articles,title=u'Dernières Nouvelles')
    else:
        return render_template('temp_intro_articles.html',articles=articles,title='Lates News', langue=1)

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

@app.route('/save/nouveau', methods=['POST','GET'])
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
def afficher_update(id_article):
    article = get_db().get_info_article(id_article)
    erreur_data = valider_acticle(article)
    photos = get_db().liste_medias()
    categories = get_db().liste_categories()
    return render_template('temp_creat_article.html', articles=article,
                               erreur_data=erreur_data, photos=photos, update='update',categories=categories)

@app.route('/save/miseajour', methods=['POST','GET'])
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
def loadupdate():
    articles = get_db().all_liste()
    return render_template('temp_listes_articles.html',articles=articles)

@app.route('/save/fichiers', methods=['POST','GET'])
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
def delete_article(id_article):
    get_db().delete_article(id_article)
    return redirect(url_for('loadupdate'))

@app.route('/article/<categorie>/<url_article>', methods=['POST','GET'])
def afficher_article(categorie,url_article):
    article=get_db().get_url_article(url_article)
    comments=get_db().get_comments(article.unique)
    if verifierLangue() == 'FR':
        return render_template('temp_article.html',articles=article,title=u'Catégorie : '+categorie,comments=comments)
    else:
        return render_template('temp_article.html',articles=article,title='Category : '+categorie, langue=1,comments=comments)

@app.route('/categorie/<id_categorie>', methods=['POST','GET'])
def afficher_article_categorie(id_categorie):
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
        get_db().save_comments('admin',content['id_article'],content['comment'])
        comments=get_db().get_comments(content['id_article'])
    return render_template('comments.html',comments=comments)

@app.route('/admin/comments', methods=['POST','GET'])
def validate_comments():
    comments=get_db().get_comments_unvalidated()
    return render_template('temps_admin_comment.html',comments=comments)

@app.route('/valider/comments/<id_comments>', methods=['POST','GET'])
def check_comments(id_comments):
    get_db().comments_validated(id_comments)
    return '',200

@app.route('/unvalider/comments/<id_comments>', methods=['POST','GET'])
def uncheck_comments(id_comments):
    get_db().comments_unvalidated(id_comments)
    return '',200

@app.route('/valider/signaler/comments/<id_comments>', methods=['POST','GET'])
def signal_comments(id_comments):
    get_db().comments_validated_signaled(id_comments)
    return '',200

@app.route('/validated/comments', methods=['POST','GET'])
def validated_comments():
    comments = get_db().get_valid_comments()
    return render_template('liste_comments.html',comments=comments)

@app.route('/unvalidated/comments', methods=['POST','GET'])
def unvalidated_comments():
    comments = get_db().get_comments_unvalidated()
    return render_template('liste_comments.html',comments=comments)

@app.route('/signaled/comments', methods=['POST','GET'])
def singaled_comments():
    comments = get_db().get_signaled_comments()
    return render_template('liste_comments.html',comments=comments)

@app.route('/all/comments', methods=['POST','GET'])
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
    return resp

@app.route('/gestion', methods=['POST','GET'])
def gestion_admin():
	return render_template('temp_menu_admin.html')

@app.route('/sidepanel/<type>', methods=['POST','GET'])
def sidepanel(type):
    if request.method == "GET":
        return 0
    else:
        return 0

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

def Log(action):
    id_user='admin'
    get_db().log_activity(id_user,action, request.user_agent.platform, request.user_agent.browser+" "+request.user_agent.version, request.environ['REMOTE_ADDR'])

def kept_search():
    search = request.cookies.get('recherche')
    return search

