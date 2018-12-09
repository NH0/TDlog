from flask import Flask, render_template, url_for

app = Flask(__name__)
app.config.from_object('config')

from .utils import find_article


@app.route('/article')
def projet():
    article_c = find_article(1)
    return render_template('projet.html',
                            title = article_c.title,
                            text = article_c.text)

@app.route('/')
@app.route('/home/')
def home():
    return render_template('home.html')
