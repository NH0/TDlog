from flask import Flask, render_template, url_for, request

app = Flask(__name__)
app.config.from_object('config')

from .utils import find_article, find_article_by_keywords
from .basicFunctions import *
from newspaper import Article

@app.route('/article', methods=['GET', 'POST'])
def projet():
    keywords = request.form['KeyWords'].replace(" ","").split(',') #créer une liste de string contenant les mots-clés
    for key in keywords:
        key = key.lower() # insensible à la casse
    article_c = find_article_by_keywords(keywords)
    stringOfKeywords = listToString(keywords)
    print(stringOfKeywords)
    if (article_c == 0):
        return render_template('erreur.html',keywords=stringOfKeywords)
    else: # Pour l'instant renvoie le premier article uniquement
        return render_template('projet.html',
                                articleList = article_c,
                                searchedKeywords = stringOfKeywords)

@app.route('/article2', methods=['GET', 'POST'])
def projetBis2():
    keywords = request.form['KeyWords'].replace(" ","").split(',') #créer une liste de string contenant les mots-clés
    for key in keywords:
        key = key.lower() # insensible à la casse
    sites = google_search_website(keywords, "", 1)
    for url in sites:
        add_article_to_db(url, keywords)
    db.session.commit()
    article_c = find_article_by_keywords(keywords)
    stringOfKeywords = listToString(keywords)
    print(stringOfKeywords)
    if (article_c == 0):
        return render_template('erreur.html',keywords=stringOfKeywords)
    else: # Pour l'instant renvoie le premier article uniquement
        return render_template('projet.html',
                                articleList = article_c,
                                searchedKeywords = stringOfKeywords)


@app.route('/', methods=['GET', 'POST'])
@app.route('/home/')
def home():
    return render_template('home.html')
