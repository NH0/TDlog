from flask import Flask, render_template, url_for

app = Flask(__name__)
app.config.from_object('config')

from .utils import *

@app.route('/projet/')
def projet():
    #article = find_article(1)
    article = random_article()
    return (render_template('projet.html',
                            title = article.title,
                            text = article.text))


if __name__ == "__main__":
    app.run()
