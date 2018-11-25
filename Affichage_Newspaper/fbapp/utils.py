import random as rd

from fbapp.models import Article

def find_article(id):
    article = Article.query.filter(Article.id == id).all()
    return rd.choice(article)
