import random as rd
from nltk.corpus import wordnet
from itertools import chain

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
        article_c = Article_c.query.filter(Article_c.keywords.ilike('%'+key+'%')).all() # on regarde si le mot-clé fait partie des mots-clés de l'article
        if(len(article_c)>0):
            articlesMatched.append(rd.choice(article_c))
    if (len(articlesMatched)>0):
        return articlesMatched
    else:
        return 0

def findSynonyms(word):
    SetOfSynonyms = wordnet.synsets(word)
    synonyms = set([]) # Unique elements
    for syn in SetOfSynonyms:
        for name in syn.lemma_names():
            synonyms.add(name)
        for hyperList in syn.hypernyms():
            for hyper in hyperList.lemma_names():
                synonyms.add(hyper)
        for hypoList in syn.hyponyms():
            for hypo in hypoList.lemma_names():
                synonyms.add(hypo)
    return (synonyms)
