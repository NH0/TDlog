import random as rd
from itertools import chain

from fbapp.models import Article_c
from .basicFunctions import *

def formatKeywords(keywords):
    """
    Rendre les mots clés insensibles à la casse
    """
    for key in keywords:
        key = key.lower()
    return keywords


def find_api(keywords, nb_article):
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
    articles = get_api(keywords, nb_article)
    length = min(nb_article, len(articles))
    print("length = {}".format(length))
    for i in range(length):
        url = articles[i]['url']
        print(url)
        title = articles[i]['title']
        description = articles[i]['description']
        source = articles[i]['source']['name']
        article = Article(url)
        article.download()
        article.parse()
        article.nlp()
        content = article.text
        articlesMatched.append(Article_c(url = url,
                                title = title,
                                text = content,
                                summary = description,
                                keywords = stringOfKeywords,
                                source_url = url,
                                site_name = source))
    return(articlesMatched)


def find_api_from(keywords, nb_article, sources):
    """
    fonction renvoyant une liste d'article (la classe Article_c) depuis une recherche google news provenant de certaines sources
    input :
    1- keywords : une liste de mots clefs de la forme ['keyword1','keyword2',...]
    2- nb_article : un entier, nombre d'articles a renvoyer
    output :
    1- articlesMatched = une liste des articles trouvés sur google news
    """
    stringOfKeywords = listToString(keywords)
    articlesMatched = []
    urls = []
    for source in sources:
        articles = get_api(keywords, nb_article, source)
        length = min(nb_article, len(articles))
        for i in range(length):
            urls.append(articles[i]['url'])

    nb_sites = len(urls)
    if nb_sites != 0:
        for i in range(nb_sites):
            url = articles[i]['url']
            print(url)
            title = articles[i]['title']
            description = articles[i]['description']
            source = articles[i]['source']['name']
            article = Article(url)
            article.download()
            article.parse()
            article.nlp()
            content = article.text
            articlesMatched.append(Article_c(url = url,
                                    title = title,
                                    text = content,
                                    summary = description,
                                    keywords = stringOfKeywords,
                                    source_url = url,
                                    site_name = source))
    return(articlesMatched)


def find_article_api_from(keywords, nb_article=2, sources=[]):
    """
    Chercher des articles dans la base de données et si besoin par recherche internet pour compléter et avoir suffisament d'articles
    à afficher
    """
    articles_list = find_article_db(keywords, sources, nb_article)  # cherche l'article dans la base de données
    nbFound = len(articles_list)

    if (nbFound < nb_article):    # si pas assez d'article ne correspondent dans la BDD, les chercher sur google news
        if len(sources)==0:
            articles_list = find_api(keywords, nb_article-nbFound)   # cherche les articles restants
        else:
            articles_list = find_api_from(keywords, nb_article-nbFound, sources) # cherche les articles avec l'api en ne gardant que les articles provenant de certains sites d'information

    articles_list = sorted(articles_list, key=lambda x: x.note, reverse=True) #Triés par préférences des utilisateurs

    return articles_list
