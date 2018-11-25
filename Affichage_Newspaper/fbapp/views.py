from flask import Flask, render_template, url_for

app = Flask(__name__)
app.config.from_object('config')

from .utils import find_article

article = find_article(1)

@app.route('/projet/')
def projet():
    return (render_template('projet.html',
                            title = article.title,
                            text = article.text))


if __name__ == "__main__":
    app.run()
