from flask_sqlalchemy import SQLAlchemy
import logging as lg
import enum
from .views import app
from .basicFunctions import listToString
import config as cf
from newspaper import Article
from googlesearch import search

# Create database connection object
db = SQLAlchemy(app)

class Article_c(db.Model):
    idarticle = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(400), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    text = db.Column(db.String(), nullable=False)
    keywords = db.Column(db.String(), nullable=False)
    # authors = db.Column(db.String(), nullable=False) A IMPLEMENTER PLUS TARD: ATTENTION, C'EST UNE LISTE D'AUTEURS QUE L'ON RECOIT GRACE A LA LIBRAIRIE PYTHON


    def __init__(self, url, title, text, keywords):
        self.url = url
        self.title = title
        self.text = text
        self.keywords = keywords
        # self.authors = authors



def google_search_website(keywords, web_site, nb_url):
    """
    input :
    1- keywords : une liste de mots clefs de la forme ['keyword1','keyword2',...]
    2- web_site : une string du site web sur lequel chercher le/les articles, ex : 'www.theguardian.com'
    3- nb_article : un entier, nombre d'url a selectionner
    output :
    1- sites = une liste des url des articles trouvés sur le web de la forme ['url1','url2',...]
    """
    query = ''
    sites = []
    for keyword in keywords:
        query += keyword + ' '
    query += 'site:' + web_site
    print(query)
    for url in search(query, tld="com", num=nb_url, stop=nb_url, pause=2):
        print(url)
        sites.append(url)
    return(sites)


keyword_example = ['air', 'france', 'klm', 'cultural', 'differences']
url_example = google_search_website(keyword_example, 'www.theguardian.com', 1)

"""
keywords doit être une liste de keywords : ['keyword1','keyword2','keyword3']
"""
def add_article_to_db(url, keywords): # Automatisation du processus pour ajouter une entrée à la base de données, pour l'instant il faut renseigner soi meme les keywords
    article = Article(url)
    article.download()
    article.parse()
    stringOfKeywords = listToString(keywords) # insensible à la casse, string avec les mots clés séparés par une ','
    db.session.add(Article_c(url = url,
                            title = article.title,
                            text = article.text,
                            keywords = stringOfKeywords))

def init_db():
    db.drop_all()
    db.create_all()
    for url in url_example:
        article = Article(url)
        article.download()
        article.parse()
        db.session.add(Article_c(url = url, title = article.title, text = article.text, keywords = listToString(keyword_example)))
    add_article_to_db('https://www.theguardian.com/media/2018/nov/16/bbc-women-complain-andrew-neil-tweet-observer-journalist-carole-cadwalladr',
                        ['Journalist','twitter','sexism'])
    add_article_to_db('https://edition.cnn.com/2018/12/08/europe/ndrangheta-mafia-raids-analysis-intl/index.html',
                        ['Mafia','analysis'])
    add_article_to_db('https://www.lemonde.fr/international/article/2018/12/09/migration-marine-le-pen-et-steve-bannon-denoncent-a-bruxelles-le-pacte-avec-le-diable_5394839_3210.html',
                        ['Migration','Marine le Pen'])
    db.session.commit()
    lg.warning('Database initialized!')
