from flask_sqlalchemy import SQLAlchemy
import logging as lg
import enum
from .views import app
import config as cf
from newspaper import Article

# Create database connection object
db = SQLAlchemy(app)

class Article_c(db.Model):
    idarticle = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(400), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    text = db.Column(db.String(), nullable=False)
    # keywords =

    def __init__(self, url, title, text):
        self.url = url
        self.title = title
        self.text = text
        # self.keywords =


def init_db():
    db.drop_all()
    db.create_all()
    url = 'https://www.theguardian.com/media/2018/nov/16/bbc-women-complain-andrew-neil-tweet-observer-journalist-carole-cadwalladr'
    article = Article(url)
    article.download()
    article.parse()
    db.session.add(Article_c(url = url,
                            title = article.title,
                            text = article.text))
    db.session.add(Article_c('https://www.bbc.com/news/uk-46334649',
                            "EU leaders agree UK's Brexit deal at Brussels summit",
                            'Toujours pas de texte'))
    db.session.commit()
    lg.warning('Database initialized!')
