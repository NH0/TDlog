from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from .utils import *
from newspaper import Article

@app.route('/article', methods=['GET', 'POST'])
def projet():
    keywords = request.form['KeyWords'].replace(" ","").split(',') #créer une liste de string contenant les mots-clés
    for key in keywords:
        key = key.lower() # insensible à la casse
    stringOfKeywords = listToString(keywords)
    article_c = find_article_by_keywords(keywords)
    if (article_c == 0):
        #article_c = find_article_online(keywords, '')
        article_c = find_article_news(keywords)
        # for article in article_c:
        #     db.session.add(article)
        # db.session.commit()
    return render_template('projet.html',
                            articleList = article_c,
                            searchedKeywords = stringOfKeywords)


@app.route('/', methods=['GET', 'POST'])
@app.route('/home/')
def home():
    return render_template('home.html')
