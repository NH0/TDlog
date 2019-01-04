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
    articleS = find_article_by_keywords(keywords)  # cherche l'article dans la base de données
    if (articleS == 0):    # si aucun article ne correspond dans la BDD, le cherche sur google news
        articleS = find_article_news(keywords, nb_article = 1)   # cherche nb_article = 1 article
        # for article in article_c:
        #     db.session.add(article)
        # db.session.commit()
    return render_template('projet.html',
                            articleList = articleS,
                            searchedKeywords = stringOfKeywords)


@app.route('/', methods=['GET', 'POST'])
@app.route('/home/')
def home():
    return render_template('home.html')
