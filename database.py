import sqlite3
from datetime import datetime
import time


class Articles:
    def __init__(self, unique, url,auteur,datepub,titre_fr,titre_ang,texte_fr,texte_ang,categorie,etiquettes,tag,photo, cat_fr, cat_ang, data1, data2):
        self.unique = unique
        self.url = url
        self.auteur = auteur
        self.datepub = datepub
        self.titre_fr = titre_fr
        self.titre_ang = titre_ang
        self.texte_fr = texte_fr
        self.texte_ang = texte_ang
        self.categorie = categorie
        self.etiquettes = etiquettes
        self.tag = tag
        self.photo = photo
        self.cat_fr = cat_fr
        self.cat_ang = cat_ang
        self.data1 = data1
        self.data2 = data2

class Users:
    def __init__(self, id, firstname, lastname, email, role, picture, status):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.picture = picture
        self.role = role
        self.status = status

class Medias:
    def __init__(self, id, creator, media, date):
        self.id = id
        self.creator = creator
        self.media = media
        self.date = date

class Categories:
    def __init__(self, id, menu_cat_fr, menu_cat_ang, date):
        self.id = id
        self.menu_cat_fr = menu_cat_fr
        self.menu_cat_ang = menu_cat_ang
        self.date = date

class Comments:
    def __init__(self, id, id_user, id_article, comments, date, approved, signal):
        self.id = id
        self.id_user = id_user
        self.id_article = id_article
        self.comments = comments
        self.date = date
        self.approved = approved
        self.signal = signal

class Interactions:
     def __init__(self,id,id_user, action, os, browser, ip_adresse, date):
        self.id = id
        self.id_user = id_user
        self.action = action
        self.os = os
        self.browser = browser
        self.ip_adresse = ip_adresse
        self.date = date

class Roles:
    def __init__(self, id, role, active):
        self.id = id
        self.role = role
        self.active = active

class Database:
    def __init__(self):
        self.connection = None

    def get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect('db/cms_db.db')
        return self.connection

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()

    def insert_article(self, url, auteur, datepub, titre_fr, titre_ang, texte_fr, texte_ang, categorie, etiquettes, tag, photo, data1, data2):
        connection = self.get_connection()
        cursor = connection.cursor()
        print "insert article"
        print data2
        print data1
        print "insert article"
        cursor.execute(("insert into article(url, auteur, datepub, titre_fr, titre_ang, texte_fr, texte_ang, categorie, etiquettes, tag, photo, data_1, data_2 ) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"),(url, auteur, datepub, titre_fr, titre_ang, texte_fr, texte_ang, categorie, etiquettes, tag,photo, data1, data2,))
        connection.commit()

    def select_liste(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("""select * from article, categories where article.categorie = categories.id and article.datepub <=(select date('now'))order by article.datepub desc""")
        listes = []
        for row in cursor:
            p = Articles(row[0],row[1],row[2],row[3], row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[17],row[18],row[12],row[13])
            listes.append(p)
        return listes

    def all_liste(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("""select * from article,categories where article.categorie = categories.id order by datepub desc""")
        listes = []
        for row in cursor:
            p = Articles(row[0],row[1],row[2],row[3], row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[17],row[18],row[12],row[13])
            listes.append(p)
        return listes

    def get_info_article(self,id):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("""select * from article, categories where article.categorie= categories.id and article.id = ?"""), (id, ))
        row = cursor.fetchone()
        p = Articles(row[0],row[1],row[2],row[3], row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[17],row[18],row[12],row[13])
        return p

    def get_url_article(self,url):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("""select * from article, categories where article.categorie= categories.id and article.url = ?"""), (url, ))
        row = cursor.fetchone()
        p = Articles(row[0],row[1],row[2],row[3], row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[17],row[18],row[12],row[13])
        print row[13]
        return p

    def get_categorie_article(self,id_categorie):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("""select * from article,categories where article.categorie=categories.id and (categories.menu_cat_fr like ? or categories.menu_cat_ang like ?) order by datepub desc"""),(id_categorie, id_categorie, ))
        listes = []
        for row in cursor:
            p = Articles(row[0],row[1],row[2],row[3], row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[17],row[18],row[12],row[13])
            listes.append(p)
        return listes

    def get_categorie_article_auteur(self,id_auteur):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("""select * from article,categories where article.categorie=categories.id and (article.auteur like ?) order by datepub desc"""),(id_auteur, ))
        listes = []
        for row in cursor:
            p = Articles(row[0],row[1],row[2],row[3], row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[17],row[18],row[12],row[13])
            listes.append(p)
        return listes

    def select_all(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("select * from article order by date_publication desc")
        listes = []
        for row in cursor:
            p = Articles(row[0], row[1], row[5], row[3], row[4], row[2])
            listes.append(p)
        return listes

    def get_json_all(self):
        cursor = self.get_connection().cursor()
        cursor.execute("select * from article order by date_publication desc")
        articles = cursor.fetchall()
        return [(un_article[0], un_article[1], un_article[2], un_article[3],
                 un_article[4], un_article[5]) for un_article in articles]

    def get_json_article(self, id_article):
        cursor = self.get_connection().cursor()
        cursor.execute(("select * from article where id = ?"), (id_article, ))
        article = cursor.fetchone()
        if article is None:
            return None
        else:
            return (article[0], article[1], article[2], article[3], article[4],
                    article[5])

    def select_recherche(self, recherche):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(( """select * from article,categories where article.categorie = categories.id and (article.texte_fr like ? or article.texte_ang like ? or article.titre_fr like ? or article.titre_ang like ? )order by datepub desc"""),("%"+recherche+"%", "%"+recherche+"%","%"+recherche+"%", "%"+recherche+"%",))
        listes = []
        for row in cursor:
            p = Articles(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10],
                         row[11], row[17], row[18], row[12],row[13])
            listes.append(p)
        return listes

    def select_url(self, url):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("select * from article where url like ?",
                       (url, ))
        row = cursor.fetchone()
        if row:
            return True
        else:
            return False

    def select_article(self, url):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("select * from article where url like ?",
                       (url, ))
        for row in cursor:
                article = Articles(row[0], row[1], row[5],
                                   row[3], row[4], row[2])
        if article is None:
            return None
        else:
            return article

    def update_article(self, unique, url,auteur,datepub,titre_fr,titre_ang,texte_fr,texte_ang,categorie,etiquettes,tag,photo,data_1, data2):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("update article set url = ?,auteur = ?,datepub = ?,titre_fr = ?,titre_ang = ?,texte_fr = ?,texte_ang = ?,categorie = ?,etiquettes = ?,tag = ?,photo = ?, data_1 = ?,data_2 = ? where id=?",
                       (url,auteur,datepub,titre_fr,titre_ang,texte_fr,texte_ang,categorie,etiquettes,tag,photo,data_1, data2, unique, ))
        connection.commit()

    def effacer_articles(self, unique):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("delete from article where id=?", (unique, ))
        connection.commit()

    def ajout_utilisateur(self, nom, courriel, salt, hash):
        connection = self.get_connection()
        connection.execute(("""insert into users(nom,courriel,salt,hash)values
                           (?,?,?,?)"""), (nom, courriel, salt, hash))
        connection.commit()

    def get_user_login_info(self, courriel):
        cursor = self.get_connection().cursor()
        cursor.execute(("select salt, hash from users where courriel=?"),
                       (courriel, ))
        user = cursor.fetchone()
        if user is None:
            return None
        else:
            return user[0], user[1]

    def save_session(self, id_session, username):
        connection = self.get_connection()
        connection.execute(("insert into sessions(id_session, courriel) "
                            "values(?, ?)"), (id_session, username))
        connection.commit()

    def delete_session(self, id_session):
        connection = self.get_connection()
        connection.execute(("delete from sessions where id_session=?"),
                           (id_session, ))
        connection.commit()

    def get_session(self, id_session):
        cursor = self.get_connection().cursor()
        cursor.execute(("select courriel from sessions where id_session=?"),
                       (id_session, ))
        data = cursor.fetchone()
        if data is None:
            return None
        else:
            return data[0]

    def save_invitation(self, courriel, token, role):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("insert into invitation(courriel, token, date_invitation, role) "
                        "values(?, ?, ?, ?)"), (courriel, token, datetime.now(), role,))
        connection.commit()

    def save_recuperation(self, courriel, token):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("insert into recuperations(courriel, token, "
                        "date_demande) values(?, ?, ?)"), (courriel, token,
                        time.mktime(datetime.now().timetuple()), ))
        connection.commit()

    def inviter_courriel(self, courriel):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("select * from invitation where courriel like ?"),
                       (courriel, ))
        data = cursor.fetchone()
        if data is None:
            return True
        else:
            return False

    def valider_courriel(self, courriel):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("select * from users where courriel like ?"),
                       (courriel, ))
        data = cursor.fetchone()
        if data is None:
            return True
        else:
            return False

    def valider_invitation(self, id_token):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("select * from invitation where token like ?"),
                       (id_token, ))
        data = cursor.fetchone()
        if data is None:
            return False
        else:
            return data

    def delete_invitation(self, token):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("delete from invitation where token=?"),
                       (token, ))
        connection.commit()

    def update_mot_passe(self, courriel, salt, hash):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("update users set salt=?, hash =? where courriel=?"),
                       (salt, hash, courriel, ))
        connection.commit()

    def courriel_session(self, id_session):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("select courriel from sessions where id_session "
                       "like ?"), (id_session, ))
        data = cursor.fetchone()
        if data is None:
            return False
        else:
            return data

    def courriel_recuperation(self, token):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("select courriel from recuperations where token "
                       "like ?"), (token, ))
        data = cursor.fetchone()
        if data is None:
            return False
        else:
            return data[0]

    def recuperer_motpasse(self, id_token):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("select date_demande from recuperations where "
                       "token like ?"), (id_token,))
        data = cursor.fetchone()
        if data is None:
            return None
        else:
            return data[0]

    def delete_recuperation(self, token):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("delete from recuperations where token=?"),
                       (token, ))
        connection.commit()

    def valider_url(self, url):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("select * from article where url like ?"),
                       (url, ))
        data = cursor.fetchone()
        if data is None:
            return False
        else:
            return True

    def valider_url_2(self, url,unique):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("select * from article where url like ? and id <> ?"),
                       (url, unique, ))
        data = cursor.fetchone()
        if data is None:
            return False
        else:
            return True

    def valider_mise_a_jour_url(self, url):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("select * from article where url like ?"),
                       (url, ))
        data = cursor.fetchone()
        if data is None:
            return False
        else:
            return True

    def token_invitation(self, courriel):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("select * from invitation where courriel like ?"),
                       (courriel, ))
        data = cursor.fetchone()
        return data[2]

    def save_medias(self, creator, filename):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("insert into medias(creator, media, "
                        "date) values(?, ?, ?)"), (creator, filename, datetime.now(), ))
        connection.commit()
        
    def valider_medias(self, filename):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("select * from medias where media like ?"),(filename, ))
        data = cursor.fetchone()
        if data is None:
            return True
        else:
            return False

    def liste_medias(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("select * from medias order by id desc"))
        listes = []
        for row in cursor:
            tempdate=row[3][:10]
            p = Medias(row[0], row[1], row[2], tempdate)
            listes.append(p)
        return listes

    def delete_medias(self,filename):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("delete from medias where media = ?"),(filename, ))
        connection.commit()

    def name_file_media(self,id):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("select * from medias"))
        data = cursor.fetchone()
        if data is None:
            return None
        else:
            return data[2]

    def liste_categories(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("select * from categories"))
        listes = []
        for row in cursor:
            tempdate=row[3][:10]
            p = Categories(row[0], row[1], row[2], tempdate)
            listes.append(p)
        return listes

    def delete_article(self,id_article):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("delete from article where id = ?"),(id_article, ))
        connection.commit()

    def log_activity(self, id_user,action, os, browser, ip_adresse):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("insert into INTERACTION(id_user, action, os, browser, ip_adresse, date) values(?, ?, ?, ?, ?, ?)"), (id_user, action, os, browser, ip_adresse, datetime.now(), ))
        connection.commit()

    def get_comments(self, id_article):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("select * from comments where id_article = ? order by date desc"),(id_article, ))
        comments = []
        for row in cursor:
            tempdate=row[4][:10]
            c = Comments(row[0], row[1], row[2], row[3], tempdate, row[5],row[6])
            comments.append(c)
        return comments

    def save_comments(self,id_user,id_article,comment,indice):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("insert into COMMENTS(id_user, id_article, indice_user, comment, date, approved, signal) values(?, ?, ?, ?, ?, ?, ? )"), (id_user, id_article, indice, comment, datetime.now(),"false","false" ))
        connection.commit()

    def get_all_comments(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("select * from comments order by date desc"))
        comments = []
        for row in cursor:
            tempdate=row[4][:10]
            c = Comments(row[0], row[1], row[2], row[3], tempdate, row[5],row[6])
            comments.append(c)
        return comments

    def get_comments_unvalidated(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("select * from comments where approved = ? and signal = ? "), ("false","false",))
        comments = []
        for row in cursor:
            tempdate=row[4][:10]
            c = Comments(row[0], row[1], row[2], row[3], tempdate, row[5],row[6])
            comments.append(c)
        return comments

    def get_valid_comments(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("select * from comments where approved like ? and signal <> ? "),("true","true",  ))
        comments = []
        for row in cursor:
            tempdate=row[4][:10]
            c = Comments(row[0], row[1], row[2], row[3], tempdate, row[5],row[6])
            comments.append(c)
        return comments

    def get_signaled_comments(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("select * from comments where signal like ?"),("true", ))
        comments = []
        for row in cursor:
            tempdate=row[4][:10]
            c = Comments(row[0], row[1], row[2], row[3], tempdate, row[5],row[6])
            comments.append(c)
        return comments

    def comments_validated(self,id_comment):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("update comments set approved = ? where id = ? "),("true", id_comment, ))
        connection.commit()

    def comments_unvalidated(self,id_comment):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("update comments set approved = ? where id = ? "),("false", id_comment, ))
        connection.commit()

    def comments_validated_signaled(self,id_comment):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("update comments set signal = ? where id = ? "),("true", id_comment, ))
        connection.commit()


    def get_categories(self, category):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("select menu_cat_ang, menu_cat_fr where id = ? "), ("true", category,))
        connection.commit()

    def last_5_articles(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("select * from article order by datepub desc limit 5"))
        comments = []
        for row in cursor:
            tempdate = row[4][:10]
            c = Comments(row[0], row[1], row[2], row[3], tempdate, row[5], row[6])
            comments.append(c)
        return comments

    def get_roles(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("select * from roles where active = ?"),("yes",))
        roles = []
        for row in cursor:
            r = Roles(row[0], row[1], row[2])
            roles.append(r)
        return roles

    def list_all_user(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("select * from users"))
        users = []
        for row in cursor:
            r = Users(row[0],"", row[1], row[2],row[6],row[7],row[8])
            users.append(r)
        return users

    def update_user(self, id, firstname, lastname, email, role, picture, status):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("update users set  nom = ?,courriel= ?,role = ?,picture = ?, active = ? where id=?",
                       (lastname, email, role, picture, status,id, ))
        connection.commit()

    def get_User_Session(self,num_session):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("select users.nom from sessions inner join users on sessions.id_session = ?",(num_session,))
        data = cursor.fetchone()
        if data is None:
            return "invited"
        else:
            return data[0]

    def get_id_User_Session(self,num_session):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("select users.nom, users.id from sessions inner join users on sessions.id_session = ?",(num_session,))
        data = cursor.fetchone()
        if data is None:
            return "0"
        else:
            return data[1]

    def get_User_Right(self,num_session):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("select users.role from sessions inner join users on sessions.id_session = ?",(num_session,))
        data = cursor.fetchone()
        if data is None:
            return "invited"
        else:
            return data[0]
        
    def get_My_Comments(self,user):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("select * from comments where id_user = ?",(user,))
        comments = []
        for row in cursor:
            tempdate=row[4][:10]
            c = Comments(row[0], row[1], row[2], row[3], tempdate, row[5],row[6])
            comments.append(c)
        return comments

    def get_all_interactions(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute('select * from INTERACTION order by date desc')
        interactions = []
        for row in cursor:
            print row[1]
            c = Interactions(row[0], row[1], row[2], row[3], row[4], row[5],row[6])
            interactions.append(c)
        return interactions