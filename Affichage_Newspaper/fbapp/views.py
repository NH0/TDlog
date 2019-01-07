from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from .utils import *
from newspaper import Article

@app.route('/article', methods=['GET', 'POST'])
def projet():
    keywords = request.form['KeyWords'].replace(" ","").split(',') # créer une liste de string contenant les mots-clés

    sources = []
    for news_site in News_Sites:
        if(request.form.get(news_site)):
            sources.append(news_site)

    for key in keywords:
        key = key.lower() # insensible à la casse
    stringOfKeywords = listToString(keywords)
    articleS = find_article_by_keywords(keywords)  # cherche l'article dans la base de données
    # articleS = find_article_by_keywords_from(keywords, checked) # cherche l'article dans la base de données en ne gardant que les articles provenant de certains sites d'information
    if (articleS == 0):    # si aucun article ne correspond dans la BDD, le cherche sur google news
        articleS = find_article_news(keywords, nb_article = 1)   # cherche nb_article = 1 article
        # for article in article_c:
        #     db.session.add(article)
        # db.session.commit()
    return render_template('projet.html',
                            articleList = articleS,
                            searchedKeywords = stringOfKeywords,
                            sources = sources)


@app.route('/', methods=['GET', 'POST'])
@app.route('/home/')
def home():
    return render_template('home.html')
