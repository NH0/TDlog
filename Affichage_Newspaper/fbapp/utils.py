import random as rd
from nltk.corpus import wordnet
from itertools import chain

from fbapp.models import Article_c
from .basicFunctions import *
from newspaper import Article



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

News_Sites = ['theguardian','nytimes','washingtonpost']

# def find_article_by_keywords_from(keywords, checked):
#     articles_found = find_article_by_keywords(keywords)
#     for k in range(len(checked)):
#         if ()
#     for article in articles_found:
#


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

def find_article_online(keywords, website):
    stringOfKeywords = listToString(keywords) # insensible à la casse, string avec les mots clés séparés par une ','
    articlesMatched = []
    sites = google_search_website(keywords, website, 1)
    for url in sites:
        article = Article(url)
        article.download()
        article.parse()
        articlesMatched.append(Article_c(url = url,
                                title = article.title,
                                text = article.text,
                                keywords = stringOfKeywords))
    return(articlesMatched)

def find_article_news(keywords, nb_article):
    """
    fonction renvoyant une liste d'article (la classe Article_c) depuis une recherche google news
    input :
    1- keywords : une liste de mots clefs de la forme ['keyword1','keyword2',...]
    2- nb_article : un entier, nombre d'articles a renvoyer
    output :
    1- articlesMatched = une liste des articles trouvés sur google news
    """
    stringOfKeywords = listToString(keywords) # insensible à la casse, string avec les mots clés séparés par une ','
    articlesMatched = []
    sites = google_news_search(keywords, nb_article = 5)
    for url in sites:
        print(url)
        article = Article(url)
        article.download()
        article.parse()
        articlesMatched.append(Article_c(url = url,
                                title = article.title,
                                text = article.text,
                                keywords = stringOfKeywords))
    return(articlesMatched)

# def find_article_news_from(keywords, nb_article_researched = 1, sources):
#     """
#     fonction renvoyant une liste d'article (la classe Article_c) depuis une recherche google news provenant de certaines sources
#     input :
#     1- keywords : une liste de mots clefs de la forme ['keyword1','keyword2',...]
#     2- nb_article : un entier, nombre d'articles a renvoyer
#     output :
#     1- articlesMatched = une liste des articles trouvés sur google news
#     """
#     stringOfKeywords = listToString(keywords) # insensible à la casse, string avec les mots clés séparés par une ','
#     articlesMatched = []
#     sites = google_news_search(keywords, nb_article_researched)
#     source_site = get_source_site_from_url(sites[0])
#     compteur = 0
#     while(source_site not in sources or compteur < nb_article_researched-1):
#         compteur += 1
#         source_site = get_source_site_from_url(sites[compteur])
#     ## A RAJOUTER: SI ON ARRIVE AU BOUT DE LA LISTE ET QUON A PAS TROUVE D'ARTICLES, IL FAUT LE PRECISER
#     url = sites[compteur]
#     article = Article(url)
#     article.download()
#     article.parse()
#     articlesMatched.append(Article_c(url = url,
#                             title = article.title,
#                             text = article.text,
#                             keywords = stringOfKeywords))
#     return(articlesMatched)
#
# def get_source_site_from_url(url):
#     L = url.split('.')
#     source_site = L[0].split('/')[2]
#     print(source_site)
