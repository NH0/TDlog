from flask_sqlalchemy import SQLAlchemy
import logging as lg
import enum
from .views import app
from newspaper import Article
from googlesearch import search

# Create database connection object
db = SQLAlchemy(app)

class Article_c(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(200), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    text = db.Column(db.String(200), nullable=False)
    # keywords =

    def __init__(self, url, title, text):
        self.url = url
        self.title = title
        self.text = text
        # self.keywords =

db.create_all()

def simple_google_search(keyword_list, web_site):
    query = ''
    sites = []
    for keyword in keyword_list:
        query += keyword + ' '
    query += 'site:' + web_site
    print(query)
    for url in search(query, tld="com", num=1, stop=1, pause=2):
        print(url)
        sites.append(url)
    return(sites)

keyword_list = ['air france', 'klm', 'cultural', 'differences']
links = simple_google_search(keyword_list, 'www.theguardian.com')

def init_db():
    db.drop_all()
    db.create_all()
    for url in links:
        article = Article(url)
        article.download()
        article.parse()
        db.session.add(Article_c(url = url, title = article.title, text = article.text))
    db.session.commit()
    lg.warning('Database initialized!')
