from flask_sqlalchemy import SQLAlchemy
import logging as lg
import enum
from .views import app

# Create database connection object
db = SQLAlchemy(app)

class Article(db.Model):
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

def init_db():
    db.drop_all()
    db.create_all()
    db.session.add(Article('https://www.theguardian.com/media/2018/nov/16/bbc-women-complain-andrew-neil-tweet-observer-journalist-carole-cadwalladr',
                            'BBC women complain after Andrew Neil tweet about Observer journalist',
                            'Pas encore de texte'))
    db.session.commit()
    lg.warning('Database initialized!')
