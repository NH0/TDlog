import random as rd
from fbapp.models import Article_c

def find_article(id):
    article = Article_c.query.filter(Article_c.id == id).all()
    return rd.choice(article)

def random_article():
    article = Article_c.query.all()
    return rd.choice(article)

def search_article(keyword):
    res=[]
    article = Article_c.query.all()
    for elem in article:
        if keyword in elem.title:
            res.append(elem)
    return rd.choice(res)
