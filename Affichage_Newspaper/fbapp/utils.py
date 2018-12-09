import random as rd

from fbapp.models import Article_c

def find_article(idarticle):
    article_c = Article_c.query.filter(Article_c.idarticle == idarticle).all()
    return rd.choice(article_c)

"""
Renvoie une liste d'articles contenant un des mots clés en argument
Si l'article n'est pas dans la base de données, renvoie 0
"""
def find_article_by_keywords(keywords): #prend en argument une liste de string contenant les mots clés
    articlesMatched = []
    for key in keywords:
        article_c = Article_c.query.filter(key in str(Article_c.keywords)).all() # on regarde si le mot-clé fait partie des mots-clés de l'article
        if(len(article_c)>0):
            articlesMatched.append(rd.choice(article_c))
    if (len(articlesMatched)>0):
        return articlesMatched
    else:
        return 0
