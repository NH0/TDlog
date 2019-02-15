from flask_sqlalchemy import SQLAlchemy
import logging as lg
import enum
from .views import app
from .basicFunctions import *
import config as cf
from newspaper import Article
from wordcloud import WordCloud
import retinasdk

# Create database connection object
db = SQLAlchemy(app)
api_key="eabe2bc0-1286-11e9-bb65-69ed2d3c7927"

class Article_c(db.Model):
    idarticle = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(400), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    text = db.Column(db.String(), nullable=False)
    keywords = db.Column(db.String(), nullable=False)
    source_url = db.Column(db.String(400), nullable=False)
    site_name = db.Column(db.String(200), nullable=False)
    summary = db.Column(db.String(), nullable=False)
    note = db.Column(db.Float(), nullable=False)
    nbVotes = db.Column(db.Integer(), nullable=False) #On a besoin du nombre de votes pour calculer la moyenne
    # authors = db.Column(db.String(), nullable=False) A IMPLEMENTER PLUS TARD: ATTENTION, C'EST UNE LISTE D'AUTEURS QUE L'ON RECOIT GRACE A LA LIBRAIRIE PYTHON

# class Article_note(db.Model):
#     idarticle = db.Column(db.Integer, primary_key=True)

    def __init__(self, url, title, text, summary, keywords, source_url, site_name):
        self.url = url
        self.title = title
        self.text = text
        self.summary = summary
        self.keywords = keywords
        self.source_url = source_url
        self.site_name = site_name
        self.note = 0.0
        self.nbVotes = 0
        # self.authors = authors

def keywords(api_key,Text):
	liteClient = retinasdk.LiteClient(api_key)
	return(liteClient.getKeywords(data("Text.txt")))

def add_article_to_db(url, keywords): # Automatisation du processus pour ajouter une entrée à la base de données, pour l'instant il faut renseigner soi meme les keywords
    liteClient = retinasdk.LiteClient(api_key)
    article = Article(url)
    article.download()
    article.parse()
    stringOfKeywords = listToString(keywords) # insensible à la casse, string avec les mots clés séparés par une ','
    db.session.add(Article_c(url = url,
                            title = article.title,
                            text = article.text,
                            summary = article.summary,
                            keywords = listToString(liteClient.getKeywords(article.text.encode('utf-8'))),
                            source_url = url,
                            site_name = article.source_url))

"""
keywords doit être une liste de keywords : ['keyword1','keyword2','keyword3']
"""

def init_db():
    db.drop_all()
    db.create_all()
    add_article_to_db('https://www.theguardian.com/media/2018/nov/16/bbc-women-complain-andrew-neil-tweet-observer-journalist-carole-cadwalladr',
                        ['Journalist','twitter','sexism'])
    add_article_to_db('https://edition.cnn.com/2018/12/08/europe/ndrangheta-mafia-raids-analysis-intl/index.html',
                        ['Mafia','analysis'])
    add_article_to_db('https://www.lemonde.fr/international/article/2018/12/09/migration-marine-le-pen-et-steve-bannon-denoncent-a-bruxelles-le-pacte-avec-le-diable_5394839_3210.html',
                        ['Migration','Marine le Pen'])
    db.session.commit()
    lg.warning('Article database initialized !')

## Définition de la table Users qui contient les identifiants et mots de passe des users
class User(db.Model):
    __bind_key__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    interests = db.Column(db.String(400), nullable=False)
    recommendation = db.Column(db.PickleType(), nullable=True)
    cloud_path = db.Column(db.String(), nullable=True)

    def __init__(self, username, password, interests, recommendation, cloud_path):
        self.username = username
        self.password = password
        self.interests = interests
        self.recommendation = recommendation
        self.cloud_path = cloud_path

# POUR INITIALISER LA BASE DE DONNEES CONTENANT LES MOTS DE PASSE, IL FAUT LANCER DANS LA CONSOLE FLASK_APP=run.py flask init_db_login
def init_db_login():
    db.drop_all(bind='users')
    db.create_all(bind='users')
    db.session.commit()
    lg.warning('User accounts database initialized !')

# Table qui contient les articles notés par chaque utilisateur et la note associée (permet d'éviter de noter 2 fois un même article)
class Votes(db.Model):
    __bind_key__ = 'votes'
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, nullable=False)
    articleid = db.Column(db.Integer, nullable=False)
    note = db.Column(db.Integer, nullable=False)

    def __init__(self, userid, articleid, note):
        self.userid = userid
        self.articleid = articleid
        self.note = note

# POUR INITIALISER LA BASE DE DONNEES CONTENANT LES MOTS DE PASSE, IL FAUT LANCER DANS LA CONSOLE FLASK_APP=run.py flask init_db_votes
def init_db_votes():
    db.drop_all(bind='votes')
    db.create_all(bind='votes')
    db.session.commit()
    lg.warning('Votes database initialized !')
