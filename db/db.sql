BEGIN TRANSACTION;
CREATE TABLE users (
	id	INTEGER PRIMARY KEY AUTOINCREMENT,
	nom	varchar2(50),
	courriel	varchar2(50),
	salt	varchar2(100),
	hash	varchar2(250),
	droit	INTEGER
);
CREATE TABLE sessions (
	id	INTEGER PRIMARY KEY AUTOINCREMENT,
	courriel	varchar2(50),
	id_session	varchar2(100)
);
CREATE TABLE recuperations ( 
	id INTEGER PRIMARY KEY AUTOINCREMENT, 
	courriel varchar2(50), 
	token varchar2(100),
	date_demande NUMERIC 
);
CREATE TABLE medias (
	id	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	creator	varchar2(50),
	media	varchar2(50) NOT NULL,
	date	varchar2(50)
);
CREATE TABLE invitation (
	id	INTEGER PRIMARY KEY AUTOINCREMENT,
	courriel	varchar2(50),
	token	varchar2(100),
	date_invitation	varchar2(50)
);
CREATE TABLE categories (
	id	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	menu_cat_fr	varchar2(50),
	menu_cat_ang	varchar2(50),
	date	varchar2(50)
);
CREATE TABLE article (
	id	INTEGER PRIMARY KEY AUTOINCREMENT,
	URL	varchar2(50),
	auteur	varchar2(100),
	datepub	varchar2(50),
	titre_fr	varchar2(50),
	titre_ang	varchar2(50),
	varchar2(50)e_fr	varchar2(500),
	varchar2(50)e_ang	varchar2(500),
	categorie	INTEGER,
	etiquettes	varchar2(50),
	tag	varchar2(50),
	photo	INTEGER
);
CREATE TABLE INTERACTION(
	id	INTEGER PRIMARY KEY AUTOINCREMENT,
	ID_USER INTEGER,
	ACTION VARCHAR2(50),
	OS VARCHAR2(50),
	BROWSER VARCHAR2(50),
	IP_ADRESSE VARCHAR2(50),
	DATE VARCHAR2(50)
	);
COMMIT;
