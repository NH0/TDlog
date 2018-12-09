from flask import Flask, render_template, url_for, request

app = Flask(__name__)
app.config.from_object('config')

from .utils import find_article, find_article_by_keywords


@app.route('/article', methods=['GET', 'POST'])
def projet():
    keywords = request.form['KeyWords']
    article_c = find_article_by_keywords(keywords)
    if (article_c == 0):
        return render_template('erreur.html',keywords=keywords)
    else:
        return render_template('projet.html',
                                title = article_c.title,
                                text = article_c.text,
                                keywords = keywords)

@app.route('/', methods=['GET', 'POST'])
@app.route('/home/')
def home():
    return render_template('home.html')
