from flask import Flask, render_template, url_for, request

app = Flask(__name__)
app.config.from_object('config')

from .utils import find_article, find_article_by_keywords, listTostring


@app.route('/article', methods=['GET', 'POST'])
def projet():
    keywords = request.form['KeyWords'].split(';') #créer une liste de string contenant les mots-clés
    for key in keywords:
        key = key.lower() # insensible à la casse
    article_c = find_article_by_keywords(keywords)
    stringOfKeywords = listTostring(keywords)
    if (article_c == 0):
        return render_template('erreur.html',keywords=stringOfKeywords)
    else: # Pour l'instant renvoie le premier article uniquement
        return render_template('projet.html',
                                title = article_c[0].title,
                                text = article_c[0].text,
                                keywords = stringOfKeywords)

@app.route('/', methods=['GET', 'POST'])
@app.route('/home/')
def home():
    return render_template('home.html')
