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
    """
    Table contenant les articles
    """
    idarticle = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(400), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    text = db.Column(db.String(), nullable=False)
    keywords = db.Column(db.String(), nullable=False)
    source_url = db.Column(db.String(400), nullable=False)
    site_name = db.Column(db.String(200), nullable=False)
    summary = db.Column(db.String(), nullable=False)
    note = db.Column(db.Float(), nullable=False)
    nbVotes = db.Column(db.Integer(), nullable=False)

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

def keywords(api_key,Text):
    """
    Renvoie les mots clés d'un texte en utilisant l'API retinasdk
    """
    liteClient = retinasdk.LiteClient(api_key)
    return(liteClient.getKeywords(data("Text.txt")))

def add_article_to_db(url):
    """
    Ajout d'un article à la base de données à partir de son url
    Le changement n'est pas "commit" par la fonction
    """
    liteClient = retinasdk.LiteClient(api_key)
    article = Article(url)
    article.download()
    article.parse()
    db.session.add(Article_c(url = url,
                            title = article.title,
                            text = article.text,
                            summary = article.summary,
                            keywords = listToString(liteClient.getKeywords(article.text.encode('utf-8'))),
                            source_url = url,
                            site_name = article.source_url))


def init_db():
    """
    Initialisation de la base de données avec 3 articles
    """
    db.drop_all()
    db.create_all()
    add_article_to_db('https://www.theguardian.com/media/2018/nov/16/bbc-women-complain-andrew-neil-tweet-observer-journalist-carole-cadwalladr')
    add_article_to_db('https://edition.cnn.com/2018/12/08/europe/ndrangheta-mafia-raids-analysis-intl/index.html')
    add_article_to_db('https://www.lemonde.fr/international/article/2018/12/09/migration-marine-le-pen-et-steve-bannon-denoncent-a-bruxelles-le-pacte-avec-le-diable_5394839_3210.html')
    db.session.commit()
    lg.warning('Article database initialized !')



class User(db.Model):
    """
    Table contenant les identifiants utilisateurs (bien sûr les mots de passe sont hashés)
    """
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

def init_db_login():
    """
    Initialisation de la table Users uniquement
    """
    db.drop_all(bind='users')
    db.create_all(bind='users')
    db.session.commit()
    lg.warning('User accounts database initialized !')



class Votes(db.Model):
    """
    Table contenant chaque vote
    """
    __bind_key__ = 'votes'
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, nullable=False)
    articleid = db.Column(db.Integer, nullable=False)
    note = db.Column(db.Integer, nullable=False)

    def __init__(self, userid, articleid, note):
        self.userid = userid
        self.articleid = articleid
        self.note = note

def init_db_votes():
    """
    Initialisation de la table Votes uniquement
    """
    db.drop_all(bind='votes')
    db.create_all(bind='votes')
    db.session.commit()
    lg.warning('Votes database initialized !')
