import random as rd
from itertools import chain

from fbapp.models import Article_c
from .basicFunctions import *
from newspaper import Article

def formatKeywords(keywords):
    for key in keywords:
        key = key.lower() # insensible à la casse
    return keywords

def find_article_db_and_news(keywords,sources=[],numberOfArticles=2):
    articles_list = find_article_db(keywords, sources,numberOfArticles)  # cherche l'article dans la base de données

    if (articles_list == 0):    # si aucun article ne correspond dans la BDD, le chercher sur google news
        if len(sources)==0:
            articles_list = find_article_news(keywords, numberOfArticles)   # cherche nb_article articles
        else:
            articles_list = find_article_news_from(keywords, numberOfArticles, sources) # cherche l'article dans la base de données en ne gardant que les articles provenant de certains sites d'information
            for article in articles_list:
                article.keyword=listToString(liteClient.getKeywords(article.text.encode('utf-8')))
                db.session.add(article)
                db.session.commit()
    articles_list = sorted(articles_list, key=lambda x: x.note, reverse=True) #Triés par préférences des utilisateurs

    return articles_list

def find_article(idarticle):
    article_c = Article_c.query.filter(Article_c.idarticle == idarticle).all()
    return rd.choice(article_c)

"""
Renvoie une liste d'articles contenant un des mots clés en argument
Si l'article n'est pas dans la base de données, renvoie 0
"""

def find_article_by_keywords(keywords, sources=[]): #prend en argument une liste de string contenant les mots clés
    articlesMatched = []
    for key in keywords:
        article_list_1 = Article_c.query.filter(Article_c.keywords.ilike('%'+key+'%')).all() # on regarde si le mot-clé fait partie des mots-clés de l'article
        if(len(article_list_1) > 0):
            if(len(sources) > 0):
                for site in sources:
                    article_list_2 = article_list_1.query.filter_by(source=site)
                    if (len(article_list_2) > 0):
                        article = rd.choice(article_list)
                        articlesMatched.append(article)
    if (len(articlesMatched)>0):
        return articlesMatched
    else:
        return 0

def find_article_db(keywords, sources,numberOfArticles=2): #prend en argument une liste de string contenant les mots clés
    articlesMatched = []
    if len(sources)>0:
        for key in keywords:
            article_list = Article_c.query.filter(Article_c.keywords.ilike('%'+key+'%'), Article_c.source_url in sources).all() # on regarde si le mot-clé fait partie des mots-clés de l'article
            if(len(article_list) > 0):
                article = rd.choice(article_list)
                articlesMatched.append(article)
    else:
        for key in keywords:
            article_list = Article_c.query.filter(Article_c.keywords.ilike('%'+key+'%')).all() # on regarde si le mot-clé fait partie des mots-clés de l'article
            if(len(article_list) > 0):
                article = rd.choice(article_list)
                articlesMatched.append(article)
    if (len(articlesMatched)>0):
        if (numberOfArticles<len(articlesMatched) and numberOfArticles>0):
            return articlesMatched[:numberOfArticles-1]
        else:
            return articlesMatched
    else:
        return 0

News_Sites = ['https://www.theguardian.com','https://www.nytimes.com','https://www.economist.com']

def find_article_online(keywords, website):
    stringOfKeywords = listToString(keywords) # insensible à la casse, string avec les mots clés séparés par une ','
    articlesMatched = []
    sites = google_search_website(keywords, website, 1)
    for url in sites:
        article = Article(url)
        article.download()
        article.parse()
        article.nlp()
        articlesMatched.append(Article_c(url = url,
                                title = article.title,
                                text = article.text,
                                summary = article.summary,
                                keywords = stringOfKeywords,
                                source_url = url,
                                site_name = article.source_url))
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
    sites = google_news_search(keywords, nb_article)
    for url in sites:
        print(url)
        article = Article(url)
        article.download()
        article.parse()
        article.nlp()
        articlesMatched.append(Article_c(url = url,
                                title = article.title,
                                text = article.text,
                                summary = article.summary,
                                keywords = stringOfKeywords,
                                source_url = url,
                                site_name = article.source_url))
    return(articlesMatched)

def find_article_news_from(keywords, nb_article_per_website, sources):
    """
    fonction renvoyant une liste d'article (la classe Article_c) depuis une recherche google news provenant de certaines sources
    input :
    1- keywords : une liste de mots clefs de la forme ['keyword1','keyword2',...]
    2- nb_article : un entier, nombre d'articles a renvoyer
    output :
    1- articlesMatched = une liste des articles trouvés sur google news
    """
    stringOfKeywords = listToString(keywords) # insensible à la casse, string avec les mots clés séparés par une ','
    articlesMatched = []
    sites = []
    for source in sources:
        url_temp = google_news_website(keywords, source, nb_article_per_website)
        for site in url_temp:
            sites.append(site)

    nb_sites = len(sites)
    if nb_sites != 0:
        ## A RAJOUTER: SI ON ARRIVE AU BOUT DE LA LISTE ET QUON A PAS TROUVE D'ARTICLES, IL FAUT LE PRECISER
        for url in sites:
            print(url)
            article = Article(url)
            article.download()
            article.parse()
            article.nlp()
            #print('meta_site_name = {}'.format(article.meta_site_name))
            articlesMatched.append(Article_c(url = url,
                                    title = article.title,
                                    text = article.text,
                                    summary = article.summary,
                                    keywords = stringOfKeywords,
                                    source_url = url,
                                    site_name = article.source_url))
        return(articlesMatched)
    else:
        articlesMatched.append(Article_c(url = '',
                                    title = "Pas de résultats",
                                    text = "Désolé, nous n'avons malheureusement pas trouvé de résultats",
                                    summary = "article.summary",
                                    keywords = "Rien du tout",
                                    source_url = "du coup y en a pas",
                                    site_name = "article.meta_site_name"))

def get_source_site_from_url(url):
    L = url.split('.')
    source_site = L[0].split('/')[2]
    print(source_site)



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
    stringOfKeywords = listToString(keywords) # insensible à la casse, string avec les mots clés séparés par une ','
    articlesMatched = []
    urls = []
    for source in sources:
        articles = get_api(keywords, nb_article, source)
        length = min(nb_article, len(articles))
        for i in range(length):
            urls.append(articles[i]['url'])

    nb_sites = len(urls)
    if nb_sites != 0:
        ## A RAJOUTER: SI ON ARRIVE AU BOUT DE LA LISTE ET QUON A PAS TROUVE D'ARTICLES, IL FAUT LE PRECISER
        for i in range(nb_article):
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
    else:
        source_url = ''
        for source in sources:
            source_url = source_url + source + ', '
        source_url = source_url[:-1]
        articlesMatched.append(Article_c(url = '',
                                    title = "no results for this combination of keywords and sources",
                                    text = "Sorry, we haven't find any article for this combination of keywords and sources",
                                    summary = "no results",
                                    keywords = stringOfKeywords,
                                    source_url = source_url,
                                    site_name = "no results"))
    return(articlesMatched)


def find_article_api_from(keywords, nb_article=2, sources=[]):
    articles_list = find_article_db(keywords, sources, nb_article)  # cherche l'article dans la base de données
    if (articles_list == 0):    # si aucun article ne correspond dans la BDD, le chercher sur google news
        if len(sources)==0:
            articles_list = find_api(keywords, nb_article)   # cherche nb_article articles
        else:
            articles_list = find_api_from(keywords, nb_article, sources) # cherche l'article dans la base de données en ne gardant que les articles provenant de certains sites d'information
            # for article in articles_list:
            #     article.keyword=listToString(liteClient.getKeywords(article.text.encode('utf-8')))
            #     db.session.add(article)
            #     db.session.commit()
    articles_list = sorted(articles_list, key=lambda x: x.note, reverse=True) #Triés par préférences des utilisateurs
    return articles_list
