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
        article_c = Article_c.query.filter(Article_c.keywords == key or Article_c.keywords == key.capitalize()).all() # Il faudrait un autre moyen de rendre les keywords des articles insensibles à la casse, dès l'enregistrement dans la BdD par exemple
        if(len(article_c)>0):
            articlesMatched.append(rd.choice(article_c))
    if (len(articlesMatched)>0):
        return articlesMatched
    else:
        return 0

def listTostring(keywords): # Pour l'affichage lorsqu'aucun article n'est trouvé
    keystring = ""
    for key in keywords:
        keystring += key + ", "
    keystring = keystring[:-2]
    return keystring
