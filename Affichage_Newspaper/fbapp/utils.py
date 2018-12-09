import random as rd

from fbapp.models import Article_c

def find_article(idarticle):
    article_c = Article_c.query.filter(Article_c.idarticle == idarticle).all()
    return rd.choice(article_c)

def find_article_by_keywords(keyword):
    article_c = Article_c.query.filter(Article_c.keywords == keyword).all()
    if(len(article_c)>0):
        return rd.choice(article_c)
    else:
        return 0
